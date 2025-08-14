"""Lightweight metrics helpers.

Supports four modes:

* ``auto`` – try Pushgateway, else export metrics via HTTP.
* ``push`` – push metrics to a Pushgateway instance.
* ``export`` – expose metrics on an HTTP endpoint.
* ``log`` – print metrics to ``stderr`` only.

The module exposes three helpers:

``mk_logger``
    Create a metric logger. It returns a ``log(name, value)`` function
    used to record numeric metrics. Mode selection is logged to
    ``stderr`` and in ``export`` mode a HTTP server is started as needed.

``mk_exec``
    Wrap ``subprocess.run`` and automatically record execution time and
    return code using a provided logger.

``push_metrics``
    Push the current registry to the configured Pushgateway. This is a
    no-op in ``log`` mode.
"""
from __future__ import annotations

import os
import sys
import time
import subprocess
import urllib.request
from typing import Callable, Iterable

__all__ = ["mk_logger", "mk_exec", "push_metrics"]

_MODE = "log"
_REGISTRY = None
_JOB = "godx"
_GATEWAY = os.environ.get("PUSHGATEWAY", "localhost:9091")
_PORT = int(os.environ.get("METRICS_EXPORT_PORT", "8000"))


def _probe(addr: str) -> bool:
    """Return ``True`` if a Pushgateway is reachable at ``addr``."""
    url = f"http://{addr}/-/ready"
    try:
        with urllib.request.urlopen(url, timeout=1):
            return True
    except Exception:
        return False


def _ensure_export(port: int, registry) -> None:
    """Start an export HTTP server if not running."""
    if getattr(_ensure_export, "_started", False):
        return
    try:
        from prometheus_client import start_http_server
    except Exception:  # pragma: no cover - missing optional dependency
        print("[metrics] prometheus_client missing; cannot export", file=sys.stderr)
        return
    start_http_server(port, registry=registry)
    _ensure_export._started = True
    print(f"[metrics] exporting on :{port}", file=sys.stderr)


def mk_logger(mode: str = "auto", job: str = "godx", *, gateway: str | None = None,
              port: int | None = None) -> Callable[[str, float], None]:
    """Return a ``log`` function configured for ``mode``.

    Parameters
    ----------
    mode:
        One of ``auto|push|export|log``.
    job:
        Job name used when pushing to gateway.
    gateway:
        Address of Pushgateway, default from ``PUSHGATEWAY`` env var.
    port:
        Port for export server, default from ``METRICS_EXPORT_PORT`` env var.
    """
    global _MODE, _REGISTRY, _JOB, _GATEWAY, _PORT

    gateway = gateway or _GATEWAY
    port = port or _PORT
    _JOB = job

    # Lazy import of prometheus_client to keep optional
    try:
        from prometheus_client import CollectorRegistry, Gauge
    except Exception:  # pragma: no cover - missing optional dependency
        CollectorRegistry = Gauge = None  # type: ignore[assignment]

    if mode == "auto":
        mode = "push" if _probe(gateway) else "export"
    if CollectorRegistry is None or Gauge is None:
        mode = "log"
    _MODE = mode
    print(f"[metrics] mode={_MODE}", file=sys.stderr)

    if _MODE in {"push", "export"}:
        _REGISTRY = CollectorRegistry()  # type: ignore[call-arg]
    else:
        _REGISTRY = None

    if _MODE == "export" and _REGISTRY is not None:
        _ensure_export(port, _REGISTRY)

    def log(name: str, value: float) -> None:
        if _MODE == "log" or _REGISTRY is None:
            print(f"[metric] {name} {value}", file=sys.stderr)
            return
        try:
            from prometheus_client import Gauge
        except Exception:  # pragma: no cover - missing optional dependency
            print(f"[metric] {name} {value}", file=sys.stderr)
            return
        Gauge(name, name, registry=_REGISTRY).set(value)

    return log


def mk_exec(logger: Callable[[str, float], None]) -> Callable[[Iterable[str] | str], subprocess.CompletedProcess]:
    """Return an ``exec`` helper that records runtime and exit code."""
    def run(cmd: Iterable[str] | str, **kwargs) -> subprocess.CompletedProcess:
        start = time.time()
        cp = subprocess.run(cmd, **kwargs)
        duration = time.time() - start
        logger("exec_seconds", duration)
        logger("exec_returncode", float(cp.returncode))
        return cp

    return run


def push_metrics(*, gateway: str | None = None, job: str | None = None) -> None:
    """Push the current registry to the Pushgateway if in push mode."""
    if _MODE != "push" or _REGISTRY is None:
        return
    gw = gateway or _GATEWAY
    jb = job or _JOB
    try:
        from prometheus_client import push_to_gateway
    except Exception:  # pragma: no cover - missing optional dependency
        print("[metrics] prometheus_client missing; cannot push", file=sys.stderr)
        return
    push_to_gateway(gw, job=jb, registry=_REGISTRY)
    print(f"[metrics] pushed to {gw} job={jb}", file=sys.stderr)


if __name__ == "__main__":
    log = mk_logger(mode=os.environ.get("METRICS_MODE", "log"))
    exec_ = mk_exec(log)
    exec_("echo metrics-smoke", shell=True, check=False)
    push_metrics()

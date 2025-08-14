"""Lightweight Prometheus metrics utilities.

Provides helpers to expose metrics in different modes:
`auto`, `push`, `export` or `log`.

Environment variables:
- `METRICS_MODE`: one of `auto|push|export|log` (default: `auto`).
- `PUSHGW_URL`: URL to a Prometheus Pushgateway.
- `METRICS_PORT`: Port for HTTP exporter when using `export` mode (default: `8000`).
"""

from __future__ import annotations

import logging
import os
import threading
import urllib.error
import urllib.request
from functools import wraps
from typing import Callable, Optional, TypeVar

try:
    from prometheus_client import (
        CollectorRegistry,
        Summary,
        push_to_gateway,
        start_http_server,
        REGISTRY,
    )
except Exception:  # pragma: no cover - library missing at runtime
    CollectorRegistry = None  # type: ignore
    Summary = REGISTRY = object  # type: ignore
    def push_to_gateway(*args, **kwargs):  # type: ignore
        raise RuntimeError("prometheus_client not installed")
    def start_http_server(*args, **kwargs):  # type: ignore
        raise RuntimeError("prometheus_client not installed")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODE = os.getenv("METRICS_MODE", "auto").lower()
PUSHGW_URL = os.getenv("PUSHGW_URL", "http://localhost:9091")
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))

_logger = logging.getLogger("metrics")
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _formatter = logging.Formatter("%(levelname)s %(message)s")
    _handler.setFormatter(_formatter)
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)

_export_started = False
_export_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _probe(url: str, timeout: float = 0.5) -> bool:
    """Return True if a Pushgateway is reachable at *url*."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:  # nosec B310
            return resp.status < 500
    except (urllib.error.URLError, ValueError):
        return False


def _ensure_export(port: int = METRICS_PORT) -> None:
    """Start the metrics HTTP exporter if not already running."""
    global _export_started
    with _export_lock:
        if _export_started:
            return
        try:
            start_http_server(port)
            _logger.info("metrics exporter started", extra={"port": port})
            _export_started = True
        except Exception as exc:  # pragma: no cover - exporter failures rare
            _logger.warning("failed to start metrics exporter", exc=exc)


# Determine final mode
if MODE == "auto":
    if PUSHGW_URL and _probe(PUSHGW_URL):
        MODE = "push"
    elif METRICS_PORT:
        MODE = "export"
        _ensure_export(METRICS_PORT)
    else:
        MODE = "log"
elif MODE == "export":
    _ensure_export(METRICS_PORT)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def mk_logger(name: str) -> logging.Logger:
    """Create a simple JSON logger with the given *name*."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


T = TypeVar("T")


def mk_exec(name: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Return decorator measuring execution time of *name* and pushing metrics."""
    metric = Summary(f"{name}_seconds", f"Execution time for {name}")

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with metric.time():
                result = func(*args, **kwargs)
            push_metrics()
            return result

        return wrapper

    return decorator


def push_metrics(registry: Optional[CollectorRegistry] = None, job: str = "omni") -> None:
    """Push metrics based on configured mode."""
    registry = registry or REGISTRY  # type: ignore
    if MODE == "push":
        try:
            push_to_gateway(PUSHGW_URL, job=job, registry=registry)
        except Exception as exc:
            _logger.warning("pushgateway unavailable", exc=exc)
    elif MODE == "log":
        # basic logging of collected metrics
        for metric in registry.collect():
            for sample in metric.samples:
                _logger.info(
                    "metric", extra={"name": sample.name, "value": sample.value}
                )
    # export mode relies on the HTTP server started earlier


__all__ = [
    "MODE",
    "PUSHGW_URL",
    "METRICS_PORT",
    "mk_logger",
    "mk_exec",
    "push_metrics",
]

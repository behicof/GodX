"""Prometheus metrics helpers.

Metrics behaviour is configured via the ``METRICS_MODE`` environment
variable which supports three modes:

``push``   - push metrics to a Prometheus Pushgateway.
``export`` - expose metrics over HTTP for scraping.
``off``    - disable metrics entirely; all operations become no-ops.

In ``push`` or ``export`` modes failures are logged as warnings.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Callable, Optional

from prometheus_client import CollectorRegistry, push_to_gateway, start_http_server

logger = logging.getLogger(__name__)

METRICS_MODE = os.getenv("METRICS_MODE", "export").lower()


class _NoOpRegistry:
    """No-op collector used when metrics are disabled.

    Any attribute access returns a callable that accepts any arguments and
    silently returns ``None``.
    """

    def __getattr__(self, _name: str) -> Callable[..., None]:
        def _noop(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover - trivial
            return None

        return _noop


def get_registry() -> CollectorRegistry | _NoOpRegistry:
    """Return a collector registry appropriate for the configured mode.

    Returns a normal :class:`CollectorRegistry` for ``push`` and ``export``
    modes, and a no-op registry for ``off`` mode so that metric interactions
    do nothing.
    """

    if METRICS_MODE == "off":
        return _NoOpRegistry()
    return CollectorRegistry()


def push_metrics(gateway: str, job: str, registry: Optional[CollectorRegistry] = None) -> None:
    """Push metrics to a Prometheus Pushgateway.

    In ``push`` mode this pushes ``registry`` to ``gateway`` under ``job``.
    Failures are logged as warnings. In other modes the call is a no-op.
    """

    if METRICS_MODE != "push":
        return
    registry = registry or get_registry()
    try:
        push_to_gateway(gateway=gateway, job=job, registry=registry)
    except Exception as exc:  # pragma: no cover - network/IO exceptions
        logger.warning("Failed to push metrics to %s: %s", gateway, exc)


def serve_metrics(port: int, registry: Optional[CollectorRegistry] = None) -> None:
    """Start an HTTP server to expose metrics.

    In ``export`` mode this starts a server on ``port`` exposing the given
    ``registry``. Failures to bind the port are logged. In other modes the
    call is a no-op.
    """

    if METRICS_MODE != "export":
        return
    registry = registry or get_registry()
    try:
        start_http_server(port, registry=registry)
    except Exception as exc:  # pragma: no cover - network/IO exceptions
        logger.warning("Failed to start metrics HTTP server on port %s: %s", port, exc)

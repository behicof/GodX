"""Simple Prometheus metrics helpers.

Provides Counter and Gauge factories backed by a shared registry. Metrics can be
exposed via an HTTP server or pushed to a Prometheus Pushgateway.
"""
from __future__ import annotations

from typing import Iterable, Optional

from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway, start_http_server

_registry = CollectorRegistry()


def init_metrics(port: Optional[int] = None, registry: CollectorRegistry | None = None) -> CollectorRegistry:
    """Initialise the metrics subsystem.

    Args:
        port: If provided, start an HTTP metrics exporter on this port.
        registry: Optional external registry to use instead of the default.

    Returns:
        The CollectorRegistry in use.
    """
    global _registry
    if registry is not None:
        _registry = registry
    if port is not None:
        start_http_server(port, registry=_registry)
    return _registry


def counter(name: str, documentation: str, labels: Optional[Iterable[str]] = None) -> Counter:
    """Create or return a Counter metric."""
    if labels:
        return Counter(name, documentation, labelnames=list(labels), registry=_registry)
    return Counter(name, documentation, registry=_registry)


def gauge(name: str, documentation: str, labels: Optional[Iterable[str]] = None) -> Gauge:
    """Create or return a Gauge metric."""
    if labels:
        return Gauge(name, documentation, labelnames=list(labels), registry=_registry)
    return Gauge(name, documentation, registry=_registry)


def push_metrics(job: str, gateway: str = "localhost:9091") -> None:
    """Push all metrics to a Prometheus Pushgateway."""
    push_to_gateway(gateway, job=job, registry=_registry)

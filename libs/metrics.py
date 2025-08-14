import os
from typing import Tuple, Dict
from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    push_to_gateway,
    start_http_server,
)


def _setup_registry() -> CollectorRegistry:
    registry = CollectorRegistry()
    mode = os.getenv("METRICS_MODE", "export")
    port = int(os.getenv("METRICS_PORT", "8000"))
    if mode == "export":
        # Expose metrics via HTTP for Prometheus to scrape.
        start_http_server(port, registry=registry)
    return registry


def mk_logger() -> Tuple[CollectorRegistry, Counter, Gauge, Counter]:
    """Create metrics for the logger service."""
    registry = _setup_registry()
    quotes = Counter(
        "omni_ingest_quotes_total",
        "Total quotes processed",
        registry=registry,
    )
    lag = Gauge(
        "omni_ingest_lag_ms",
        "Lag in milliseconds",
        registry=registry,
    )
    errors = Counter(
        "omni_ingest_errors_total",
        "Total ingest errors",
        registry=registry,
    )
    return registry, quotes, lag, errors


def mk_exec() -> Tuple[CollectorRegistry, Histogram, Counter]:
    """Create metrics for the execution orchestrator."""
    registry = _setup_registry()
    latency_hist = Histogram(
        "omni_exec_latency_ms",
        "Execution latency in milliseconds",
        registry=registry,
        buckets=(50, 100, 200, 500, 1000),
    )
    fills = Counter(
        "omni_exec_fills_total",
        "Number of fills",
        ["symbol"],
        registry=registry,
    )
    return registry, latency_hist, fills


def push_metrics(registry: CollectorRegistry, labels: Dict[str, str]) -> None:
    """Push metrics to a Prometheus Pushgateway if configured.

    When METRICS_MODE is set to 'push', metrics are pushed to the
    gateway specified by PUSHGATEWAY_URL. In 'export' mode this
    function is a no-op since metrics are already exposed via HTTP.
    """
    mode = os.getenv("METRICS_MODE", "export")
    if mode == "push":
        gateway = os.getenv("PUSHGATEWAY_URL", "localhost:9091")
        push_to_gateway(gateway, job="godx", registry=registry, grouping_key=labels)

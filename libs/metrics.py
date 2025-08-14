"""Prometheus metrics utilities."""
from __future__ import annotations

from typing import Dict, Mapping, Iterable

from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry, push_to_gateway

PUSHGATEWAY = "pushgateway:9091"
JOB = "omni"


def reg() -> CollectorRegistry:
    """Create a new CollectorRegistry.

    Returns:
        CollectorRegistry: An empty registry for metrics.
    """
    return CollectorRegistry()


def counters(
    registry: CollectorRegistry,
    metrics: Mapping[str, str],
) -> Dict[str, Counter]:
    """Create counter metrics with a ``component`` label.

    Args:
        registry: Registry to which metrics will be registered.
        metrics: Mapping of metric name to description.

    Returns:
        Dict[str, Counter]: Mapping of names to ``Counter`` instances.
    """
    return {
        name: Counter(name, desc, ["component"], registry=registry)
        for name, desc in metrics.items()
    }


def gauges(
    registry: CollectorRegistry,
    metrics: Mapping[str, str],
) -> Dict[str, Gauge]:
    """Create gauge metrics with a ``component`` label."""
    return {
        name: Gauge(name, desc, ["component"], registry=registry)
        for name, desc in metrics.items()
    }


def hists(
    registry: CollectorRegistry,
    metrics: Mapping[str, str],
    buckets: Iterable[float] | None = None,
) -> Dict[str, Histogram]:
    """Create histogram metrics with a ``component`` label."""
    return {
        name: Histogram(name, desc, ["component"], registry=registry, buckets=buckets)
        for name, desc in metrics.items()
    }


def push(registry: CollectorRegistry, instance: str, gateway: str = PUSHGATEWAY, job: str = JOB) -> None:
    """Push metrics in ``registry`` to the Pushgateway.

    Args:
        registry: Metrics registry.
        instance: Instance identifier used as grouping key.
        gateway: Pushgateway address. Defaults to ``pushgateway:9091``.
        job: Job name. Defaults to ``omni``.
    """
    push_to_gateway(gateway, job=job, grouping_key={"instance": instance}, registry=registry)

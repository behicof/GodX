"""Prometheus metrics helpers."""
from __future__ import annotations

from typing import Dict

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, push_to_gateway

GATEWAY = "pushgateway:9091"
JOB = "omni"


def reg() -> CollectorRegistry:
    """Return a fresh CollectorRegistry."""
    return CollectorRegistry()


def counters(registry: CollectorRegistry, *names: str) -> Dict[str, Counter]:
    """Create Counter metrics with a ``component`` label."""
    return {
        name: Counter(name, f"{name} counter", ["component"], registry=registry)
        for name in names
    }


def gauges(registry: CollectorRegistry, *names: str) -> Dict[str, Gauge]:
    """Create Gauge metrics with a ``component`` label."""
    return {
        name: Gauge(name, f"{name} gauge", ["component"], registry=registry)
        for name in names
    }


def hists(registry: CollectorRegistry, *names: str) -> Dict[str, Histogram]:
    """Create Histogram metrics with a ``component`` label."""
    return {
        name: Histogram(name, f"{name} histogram", ["component"], registry=registry)
        for name in names
    }


def push(registry: CollectorRegistry, instance: str) -> None:
    """Push all metrics in *registry* to the Pushgateway.

    Parameters
    ----------
    registry:
        Registry holding the metrics to push.
    instance:
        The ``instance`` grouping key for the push gateway.
    """
    push_to_gateway(GATEWAY, job=JOB, registry=registry, grouping_key={"instance": instance})

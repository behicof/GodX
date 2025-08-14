import collections

COUNTERS = collections.defaultdict(int)
GAUGES = {}


def reg(name: str) -> None:
    """Register a metrics namespace (no-op for stub)."""
    return None


def counters(metric: str, typ: str) -> None:
    """Increment counter identified by metric and type."""
    key = (metric, typ)
    COUNTERS[key] += 1


def gauges(metric: str, value: int) -> None:
    """Set gauge value for metric."""
    GAUGES[metric] = value


def push() -> None:
    """Push metrics to backend (stub)."""
    return None

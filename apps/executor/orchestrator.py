import random
import time

from prometheus_client import CollectorRegistry, Counter, Histogram, push_to_gateway

# Metric registry and instruments
reg = CollectorRegistry()

counters = {
    "events": Counter("events", "Number of events", ["label"], registry=reg),
    "errors": Counter("errors", "Number of errors", registry=reg),
}

hists = {
    "leg_latency": Histogram(
        "leg_latency", "Latency per leg in milliseconds", registry=reg
    )
}

def push() -> None:
    """Push metrics to the local Prometheus Pushgateway.

    The push operation is wrapped in a try/except block so running this module
    does not crash if no Pushgateway is available.
    """
    try:
        push_to_gateway("localhost:9091", job="executor", registry=reg)
    except Exception:
        pass

def main() -> None:
    for _ in range(5):
        latency_ms = random.randint(80, 600)
        hists["leg_latency"].observe(latency_ms)
        counters["events"].labels("trade_attempt").inc()
        if random.random() < 0.05:
            counters["errors"].inc()
        push()
        time.sleep(1)
    print("orchestrator: metrics pushed")

if __name__ == "__main__":
    main()

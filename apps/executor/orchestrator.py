"""Simple orchestrator emitting metrics."""

import random
import time

from metrics import reg, counters, hists, push


# Register metrics
reg("events", kind="counter", description="Number of executor events", labels=["type"])
reg("errors", kind="counter", description="Number of executor errors")
reg("leg_latency", kind="histogram", description="Latency per leg in milliseconds")


def main() -> None:
    """Emit metrics for five trade attempts."""
    for _ in range(5):
        leg_latency = random.randint(80, 600)
        hists["leg_latency"].observe(leg_latency)
        counters["events"].labels("trade_attempt").inc()
        if random.random() < 0.05:
            counters["errors"].inc()
        push()
        time.sleep(1)
    print("orchestrator: metrics pushed")


if __name__ == "__main__":
    main()

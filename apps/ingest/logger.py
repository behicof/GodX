import random
import time

try:
    from metrics import reg, counters, gauges, push
except ImportError:  # Fallback stubs if metrics package is unavailable
    def reg(*args, **kwargs):
        pass

    def counters(name: str, labels: dict | None = None, value: int = 1):
        labels = labels or {}
        print(f"counter {name} {labels} += {value}")

    def gauges(name: str, value: float):
        print(f"gauge {name} = {value}")

    def push():
        print("metrics pushed")


reg("logger")

for _ in range(3):
    counters("events", {"type": "quote_batch"})
    gauges("lag_ms", random.randint(20, 200))
    push()
    time.sleep(1)

print("logger: metrics pushed")

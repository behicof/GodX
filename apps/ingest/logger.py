import random
import time

from metrics import reg, counters, gauges, push


def main() -> None:
    reg("ingest")
    for _ in range(3):
        counters("events", "quote_batch")
        gauges("lag_ms", random.randint(20, 200))
        push()
        time.sleep(1)
    print("logger: metrics pushed")


if __name__ == "__main__":
    main()

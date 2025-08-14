import os
import time
import random
from libs.metrics import mk_logger, push_metrics
from libs.logging_utils import get_logger

PORT = int(os.getenv("METRICS_PORT", "8001"))
log = get_logger("logger")

if __name__ == "__main__":
    reg, quotes, lag, errors = mk_logger()
    log.info(f"logger service started on port {PORT}")
    while True:
        quotes.inc()
        lag.set(random.randint(5, 150))
        push_metrics(reg, {"script": "logger"})
        time.sleep(2)

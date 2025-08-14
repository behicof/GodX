import os
import time
import random
from libs.metrics import mk_exec, push_metrics
from libs.logging_utils import get_logger

PORT = int(os.getenv("METRICS_PORT", "8002"))
log = get_logger("orchestrator")

if __name__ == "__main__":
    reg, latency_hist, fills = mk_exec()
    log.info(f"orchestrator service started on port {PORT}")
    symbols = ["BTCUSDT", "ETHUSDT"]
    while True:
        sym = random.choice(symbols)
        latency = random.randint(50, 500)
        latency_hist.observe(latency)
        fills.labels(symbol=sym).inc()
        push_metrics(reg, {"script": "orchestrator"})
        time.sleep(3)

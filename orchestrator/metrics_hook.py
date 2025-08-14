import time
from libs.metrics import make_executor_metrics, push_metrics
r, leg_hist, fills_c = make_executor_metrics()

def time_leg(fn, *a, **k):
    t0 = time.time()
    res = fn(*a, **k)
    leg_hist.observe((time.time()-t0)*1000.0)
    return res

def mark_fill(symbol: str, qty: float):
    fills_c.labels(symbol=symbol).inc()
    push_metrics(r, grouping_key={"script":"orchestrator"})

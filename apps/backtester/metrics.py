import time
from libs.metrics import make_backtest_metrics, push_metrics
r, pnl_g, step_h, runs_c = make_backtest_metrics()

def run_backtest(bt):
    runs_c.inc()
    for step in bt:
        t0 = time.time()
        # ... اجرای step
        step_h.observe(time.time()-t0)
    pnl_g.set(bt.pnl())
    push_metrics(r, grouping_key={"script":"backtest"})

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, push_to_gateway
import os, time

PUSHGW = os.getenv("PUSHGW_URL", "http://localhost:9091")
JOB     = os.getenv("METRICS_JOB", "omni-scripts")
INST    = os.getenv("METRICS_INSTANCE", os.uname().nodename)

def _reg():
    r = CollectorRegistry()
    return r

def push_metrics(reg, job=JOB, grouping_key=None):
    gk = {"instance": INST}
    if grouping_key: gk.update(grouping_key)
    push_to_gateway(PUSHGW, job=job, registry=reg, grouping_key=gk)

def make_logger_metrics():
    r = _reg()
    quotes = Counter("omni_ingest_quotes_total", "Quotes ingested", registry=r)
    lag_ms = Gauge("omni_quotes_lag_ms", "Latest quotes lag (ms)", registry=r)
    errs   = Counter("omni_error_total", "Errors", registry=r)
    return r, quotes, lag_ms, errs

def make_executor_metrics():
    r = _reg()
    leg_lat = Histogram("omni_executor_leg_latency_ms", "Leg latency (ms)",
                        buckets=(50,100,200,300,500,700,900,1200,2000), registry=r)
    fills   = Counter("omni_executor_fills_total","Fills", ["symbol"], registry=r)
    return r, leg_lat, fills

def make_backtest_metrics():
    r = _reg()
    pnl = Gauge("omni_backtest_pnl", "Backtest PnL (quote ccy)", registry=r)
    step = Histogram("omni_backtest_step_seconds", "Step duration (s)",
                     buckets=(0.01,0.05,0.1,0.5,1,2,5), registry=r)
    runs = Counter("omni_backtest_runs_total","Backtest runs", registry=r)
    return r, pnl, step, runs

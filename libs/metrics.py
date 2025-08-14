from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, push_to_gateway
import os, platform

PUSHGW = os.getenv("PUSHGW_URL", "http://localhost:9091")
JOB     = os.getenv("METRICS_JOB", "omni")
INST    = os.getenv("METRICS_INSTANCE", platform.node())


def _reg():
    return CollectorRegistry()


def push_metrics(reg, job=JOB, grouping_key=None):
    gk = {"instance": INST}
    gk.update(grouping_key or {})
    push_to_gateway(PUSHGW, job=job, registry=reg, grouping_key=gk)


def mk_logger():
    r = _reg()
    return (
        r,
        Counter("omni_ingest_quotes_total", "quotes", registry=r),
        Gauge("omni_quotes_lag_ms", "lag(ms)", registry=r),
        Counter("omni_error_total", "errors", registry=r),
    )


def mk_exec():
    r = _reg()
    return (
        r,
        Histogram(
            "omni_executor_leg_latency_ms",
            "leg latency(ms)",
            buckets=(50, 100, 200, 300, 500, 700, 900, 1200, 2000),
            registry=r,
        ),
        Counter("omni_executor_fills_total", "fills", ["symbol"], registry=r),
    )


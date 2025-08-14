import os
from prometheus_client import CollectorRegistry, Counter, push_to_gateway

def main() -> None:
    gateway = os.environ.get("PUSHGW_URL", "http://localhost:9091")
    job = os.environ.get("METRICS_JOB", "omni-scripts")
    registry = CollectorRegistry()
    trades = Counter(
        "omni_backtest_trades_total",
        "Number of trades executed in backtest",
        registry=registry,
    )
    trades.inc()
    push_to_gateway(gateway, job=job, registry=registry)

if __name__ == "__main__":
    main()

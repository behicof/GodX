import os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

def main() -> None:
    gateway = os.environ.get("PUSHGW_URL", "http://localhost:9091")
    job = os.environ.get("METRICS_JOB", "omni-scripts")
    registry = CollectorRegistry()
    lag = Gauge(
        "omni_quotes_lag_ms",
        "Quote ingestion lag in milliseconds",
        registry=registry,
    )
    lag.set(1)
    push_to_gateway(gateway, job=job, registry=registry)

if __name__ == "__main__":
    main()

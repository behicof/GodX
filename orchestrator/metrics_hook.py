import os
from prometheus_client import CollectorRegistry, Histogram, push_to_gateway

def main() -> None:
    gateway = os.environ.get("PUSHGW_URL", "http://localhost:9091")
    job = os.environ.get("METRICS_JOB", "omni-scripts")
    registry = CollectorRegistry()
    latency = Histogram(
        "omni_executor_leg_latency_ms",
        "Latency per execution leg in milliseconds",
        registry=registry,
    )
    latency.observe(0.5)
    push_to_gateway(gateway, job=job, registry=registry)

if __name__ == "__main__":
    main()

import os
import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


def main() -> None:
    pushgw = os.environ.get("PUSHGW_URL", "http://localhost:9091")
    job = os.environ.get("METRICS_JOB", "omni-scripts")
    registry = CollectorRegistry()
    g = Gauge("omni_orchestrator_ping", "Dummy orchestrator metric", registry=registry)
    g.set(int(time.time()))
    push_to_gateway(pushgw, job=job, registry=registry)


if __name__ == "__main__":
    main()

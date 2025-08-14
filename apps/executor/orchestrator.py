import os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

PUSHGATEWAY = os.getenv("PUSHGATEWAY_URL", "localhost:9091")


def main() -> None:
    registry = CollectorRegistry()
    gauge = Gauge("orchestrator_runs", "Dummy orchestrator run", registry=registry)
    gauge.set(1)
    try:
        push_to_gateway(PUSHGATEWAY, job="orchestrator", registry=registry)
    except Exception as exc:  # pragma: no cover - network issues are non-critical
        print(f"Pushgateway unreachable: {exc}")


if __name__ == "__main__":
    main()

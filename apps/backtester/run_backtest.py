import os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


def main() -> None:
    registry = CollectorRegistry()
    g = Gauge("job_last_success_timestamp", "Last time job ran", registry=registry)
    g.set_to_current_time()
    gateway = os.environ.get("PUSHGATEWAY_URL", "localhost:9091")
    push_to_gateway(gateway, job="backtest", registry=registry)
    print(f"[backtest] Pushed metrics to {gateway}")


if __name__ == "__main__":
    main()

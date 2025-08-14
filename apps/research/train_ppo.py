import argparse
import os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--epochs", type=int, default=10)
    args = parser.parse_args()
    registry = CollectorRegistry()
    g = Gauge("job_last_success_timestamp", "Last time job ran", registry=registry)
    g.set_to_current_time()
    gateway = os.environ.get("PUSHGATEWAY_URL", "localhost:9091")
    push_to_gateway(gateway, job="train_ppo", registry=registry)
    print(f"[train_ppo] symbol={args.symbol} epochs={args.epochs} metrics pushed to {gateway}")


if __name__ == "__main__":
    main()

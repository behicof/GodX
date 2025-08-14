import argparse
import os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

PUSHGATEWAY = os.getenv("PUSHGATEWAY_URL", "localhost:9091")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--epochs", type=int, default=10)
    args = parser.parse_args()

    registry = CollectorRegistry()
    gauge = Gauge("train_ppo_epochs", "Number of training epochs", registry=registry)
    gauge.set(args.epochs)
    try:
        push_to_gateway(PUSHGATEWAY, job="train_ppo", registry=registry)
    except Exception as exc:  # pragma: no cover - network issues are non-critical
        print(f"Pushgateway unreachable: {exc}")


if __name__ == "__main__":
    main()

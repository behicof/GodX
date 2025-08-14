from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway as push


def main() -> None:
    """Run a sample backtest and push metrics."""
    reg = CollectorRegistry()

    gauges = {
        "pnl_daily": Gauge("pnl_daily", "Daily PnL", registry=reg),
    }
    gauges["pnl_daily"].set(12.34)

    counters = {
        "events": Counter("events", "Event counter", ["label"], registry=reg),
    }
    counters["events"].labels("backtest_done").inc()

    push("http://localhost:9091", job="backtest", registry=reg)
    print("backtest: metrics pushed")


if __name__ == "__main__":
    main()

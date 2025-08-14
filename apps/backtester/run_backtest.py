from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway as push


def main() -> None:
    """Run a simple backtest and push metrics."""
    reg = CollectorRegistry()
    gauges = {"pnl_daily": Gauge("pnl_daily", "Daily profit and loss", registry=reg)}
    counters = {
        "events": Counter("events", "Number of events", ["event"], registry=reg)
    }

    gauges["pnl_daily"].set(12.34)
    counters["events"].labels(event="backtest_done").inc()

    push("localhost:9091", job="backtester", registry=reg)
    print("backtest: metrics pushed")


if __name__ == "__main__":
    main()

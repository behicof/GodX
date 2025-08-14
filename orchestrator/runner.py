import time, random
from core.execution.executor import Executor
from core.execution.funding_arb import scan_opportunities, execute
from libs.metrics import mk_logger, push_metrics


r, quotes_c, lag_g, err_c = mk_logger()


CFG = {
    "thresholds": {
        "funding_arb": {
            "min_net_edge_bps": 300,
            "max_leg_latency_ms": 800,
            "max_slippage_bps": 35,
        }
    },
    "quotes": {},
}


def mock_market():
    spot = 30000.0 + random.uniform(-20, 20)
    perp = spot + random.uniform(-5, 5)
    funding_bps = random.choice([150, 220, 280, 320, 380, 420])
    return spot, perp, funding_bps


def loop():
    exe = Executor(mode="paper")
    while True:
        try:
            spot, perp, f_bps = mock_market()
            CFG["quotes"]["BTCUSDT"] = {"spot": spot, "perp": perp}
            funding = {"BTCUSDT": {"funding_bps": f_bps}}

            quotes_c.inc()
            lag_g.set(100)
            push_metrics(r, grouping_key={"script": "runner"})

            opps = scan_opportunities(CFG["quotes"], funding, CFG)
            for op in opps:
                res = execute(op, exe, CFG)
                # (real: log trade/PNL)
        except Exception:
            err_c.inc()
            push_metrics(r, grouping_key={"script": "runner", "err": "1"})
        time.sleep(2)


if __name__ == "__main__":
    loop()


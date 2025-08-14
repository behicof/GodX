import time, random
from libs.metrics import mk_exec, push_metrics


r, leg_hist, fills_c = mk_exec()


class Executor:
    def __init__(self, exchange=None, mode="paper"):
        self.exchange = exchange
        self.mode = mode

    def execute(
        self, symbol: str, side: str, quantity: float, price: float | None = None
    ) -> dict:
        if self.exchange is not None:
            return self.exchange.place_order(symbol, side, quantity, price)
        leg = {"side": side, "symbol": symbol, "px": price or 0}
        return self.place_ioc_pair(leg, leg, 0, 0)

    def place_ioc_pair(
        self, leg1: dict, leg2: dict, max_latency_ms: int, max_slippage_bps: int
    ):
        t0 = time.time()
        time.sleep(random.uniform(0.05, 0.18))  # simulate leg1
        leg_hist.observe((time.time() - t0) * 1000.0)
        # simulate leg2; maybe fail 5%
        t1 = time.time()
        time.sleep(random.uniform(0.05, 0.18))
        leg2_ok = random.random() > 0.05
        leg_hist.observe((time.time() - t1) * 1000.0)
        if not leg2_ok:
            push_metrics(r, grouping_key={"script": "exec", "result": "rollback"})
            return {"ok": False, "rollback": True}
        fills_c.labels(symbol=leg1.get("symbol", "?")).inc()
        push_metrics(r, grouping_key={"script": "exec", "result": "filled"})
        return {"ok": True, "filled": True}

    def get_balances(self):
        return {"USDT": 10_000, "BTC": 0.0}


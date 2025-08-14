import time, random
from core.exchange.base import Exchange
from libs.metrics import mk_exec, push_metrics

r, leg_hist, fills_c = mk_exec()

class Executor:
    def __init__(self, exchange: Exchange | None = None, mode: str = "paper"):
        self.exchange = exchange
        self.mode = mode

    def execute(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict:
        if self.exchange is None:
            return {"status": "no-exchange"}
        return self.exchange.place_order(symbol, side, quantity, price)

    def place_ioc_pair(self, leg1:dict, leg2:dict, max_latency_ms:int, max_slippage_bps:int):
        t0=time.time(); time.sleep(random.uniform(0.05,0.18))  # simulate leg1
        leg_hist.observe((time.time()-t0)*1000.0)
        # simulate leg2; maybe fail 5%
        t1=time.time(); time.sleep(random.uniform(0.05,0.18))
        leg2_ok = random.random()>0.05
        leg_hist.observe((time.time()-t1)*1000.0)
        if not leg2_ok:
            # fail-safe: close leg1 (paper)
            push_metrics(r, grouping_key={"script":"exec","result":"rollback"})
            return {"ok": False, "rollback": True}
        fills_c.labels(symbol=leg1.get("symbol","?")).inc()
        push_metrics(r, grouping_key={"script":"exec","result":"filled"})
        return {"ok": True, "filled": True}

    def get_balances(self):
        return {"USDT": 10_000, "BTC": 0.0}

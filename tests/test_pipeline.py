from orchestrator.pipeline import Pipeline
from core.exchange.base import Exchange


class DummyExchange(Exchange):
    def __init__(self):
        self.orders = []

    def place_order(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict:
        self.orders.append((symbol, side, quantity, price))
        return {"status": "filled"}


def test_pipeline_executes_order():
    exchange = DummyExchange()
    pipe = Pipeline(exchange)
    result = pipe.run({"symbol": "BTCUSDT", "side": "BUY", "qty": 1})
    assert result["status"] == "filled"
    assert exchange.orders[0][0] == "BTCUSDT"


def test_pipeline_rejects_when_risk_limit_hit():
    exchange = DummyExchange()
    cfg = {"max_notional_usd": 10, "max_sym_exposure_usd": 100, "max_exposure_usd": 100}
    pipe = Pipeline(exchange, risk_cfg=cfg)
    result = pipe.run({
        "symbol": "BTCUSDT",
        "side": "BUY",
        "qty": 1,
        "price": 20,
        "notional_usd": 20,
        "sym_exposure_usd": 0,
        "ex_exposure_usd": 0,
    })
    assert result["status"] == "rejected"
    assert "notional" in result["reason"]

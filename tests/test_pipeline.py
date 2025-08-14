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
    assert result.ok
    assert exchange.orders[0][0] == "BTCUSDT"


class FailingExchange(Exchange):
    def __init__(self):
        self.calls = 0
        self.orders = []

    def place_order(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict:
        self.calls += 1
        if self.calls == 2:
            raise RuntimeError("leg2 failure")
        self.orders.append((symbol, side, quantity, price))
        return {"status": "filled"}


def test_leg2_failure_rolls_back_leg1():
    exchange = FailingExchange()
    pipe = Pipeline(exchange)
    opportunity = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "qty": 1,
        "leg2": {"symbol": "ETHUSDT", "side": "SELL", "qty": 1},
    }
    result = pipe.run(opportunity)
    assert not result.ok
    assert exchange.orders == [
        ("BTCUSDT", "BUY", 1, None),
        ("BTCUSDT", "SELL", 1, None),
    ]

from orchestrator.pipeline import Pipeline
from core.exchange.base import Exchange


class DummyExchange(Exchange):
    def __init__(self):
        self.orders = []

    def place_order(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict:
        raise NotImplementedError

    def place_order_ioc(
        self, symbol: str, side: str, quantity: float, price: float | None = None
    ) -> dict:
        self.orders.append((symbol, side, quantity, price))
        return {"status": "filled"}


def test_pipeline_executes_order():
    exchange = DummyExchange()
    pipe = Pipeline(exchange)
    opportunity = {
        "legs": [
            {"symbol": "BTCUSDT", "side": "BUY", "qty": 1},
            {"symbol": "ETHUSDT", "side": "SELL", "qty": 1},
        ]
    }
    result = pipe.run(opportunity)
    assert result.ok
    assert exchange.orders[0][0] == "BTCUSDT"
    assert exchange.orders[1][0] == "ETHUSDT"

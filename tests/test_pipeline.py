from orchestrator.pipeline import Pipeline
from core.exchange.base import Exchange


class DummyExchange(Exchange):
    def __init__(self):
        self.orders = []

    def place_order(
        self, symbol: str, side: str, quantity: float, price: float | None = None
    ) -> dict:
        self.orders.append((symbol, side, quantity, price))
        return {"status": "filled"}


def test_pipeline_executes_order():
    exchange = DummyExchange()
    pipe = Pipeline(
        exchange,
        {"trade_limit_usd": 1000, "symbol_limit_usd": 2000, "exchange_limit_usd": 5000},
    )
    result = pipe.run(
        {"symbol": "BTCUSDT", "side": "BUY", "qty": 1, "price": 500}, 0, 0
    )
    assert result["status"] == "filled"
    assert exchange.orders[0][0] == "BTCUSDT"


def test_pipeline_rejects_over_limit():
    exchange = DummyExchange()
    pipe = Pipeline(
        exchange,
        {"trade_limit_usd": 100, "symbol_limit_usd": 200, "exchange_limit_usd": 500},
    )
    result = pipe.run(
        {"symbol": "ETHUSDT", "side": "BUY", "qty": 1, "price": 150}, 0, 0
    )
    assert result["status"] == "rejected"
    assert result["reason"] == "TRADE_LIMIT"

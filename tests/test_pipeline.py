from orchestrator.pipeline import ExecutionResult, Pipeline
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
    assert isinstance(result, ExecutionResult)
    assert result.status == "filled"
    assert result.details["status"] == "filled"
    assert result.opportunity["symbol"] == "BTCUSDT"
    assert exchange.orders[0][0] == "BTCUSDT"


def test_pipeline_rejects_order():
    exchange = DummyExchange()
    pipe = Pipeline(exchange)
    result = pipe.run({"symbol": "BTCUSDT", "side": "BUY", "qty": 0})
    assert isinstance(result, ExecutionResult)
    assert result.status == "rejected"
    assert result.details["reason"] == "risk_check_failed"
    assert result.opportunity["qty"] == 0
    assert exchange.orders == []

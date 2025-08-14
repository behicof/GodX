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


class FailingExchange(Exchange):
    def place_order(
        self, symbol: str, side: str, quantity: float, price: float | None = None
    ) -> dict:
        raise RuntimeError("boom")


class FlakyExchange(Exchange):
    def __init__(self):
        self.calls = 0

    def place_order(
        self, symbol: str, side: str, quantity: float, price: float | None = None
    ) -> dict:
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("temporary")
        return {"status": "filled"}


def test_pipeline_executes_order():
    exchange = DummyExchange()
    pipe = Pipeline(exchange)
    result = pipe.run({"symbol": "BTCUSDT", "side": "BUY", "qty": 1})
    assert result["status"] == "filled"
    assert exchange.orders[0][0] == "BTCUSDT"


def test_pipeline_handles_exchange_error():
    exchange = FailingExchange()
    pipe = Pipeline(exchange)
    result = pipe.run({"symbol": "BTCUSDT", "side": "BUY", "qty": 1})
    assert result["status"] == "error"
    assert "boom" in result["detail"]


def test_pipeline_retries_transient_failure():
    exchange = FlakyExchange()
    pipe = Pipeline(exchange)
    pipe.executor.retries = 1
    result = pipe.run({"symbol": "BTCUSDT", "side": "BUY", "qty": 1})
    assert result["status"] == "filled"
    assert exchange.calls == 2

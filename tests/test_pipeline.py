from orchestrator.pipeline import Pipeline, PipelineResult
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
    assert isinstance(result, PipelineResult)
    assert result.accepted is True
    assert result.execution == {"status": "filled"}
    assert exchange.orders[0][0] == "BTCUSDT"


def test_pipeline_rejects_order():
    exchange = DummyExchange()
    pipe = Pipeline(exchange)
    result = pipe.run({"symbol": "BTCUSDT", "side": "BUY", "qty": 0})
    assert result.accepted is False
    assert result.reason == "rejected"
    assert result.execution is None


class FailingExchange(Exchange):
    def place_order(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict:
        raise RuntimeError("boom")


def test_pipeline_exec_fail_logs_and_returns(caplog):
    exchange = FailingExchange()
    pipe = Pipeline(exchange)
    with caplog.at_level("ERROR", logger="omni"):
        result = pipe.run({"symbol": "BTCUSDT", "side": "BUY", "qty": 1})
    assert result.accepted is False
    assert result.reason == "exec_fail"
    assert result.execution is None
    assert any("exec_fail" in record.message for record in caplog.records)

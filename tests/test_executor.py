from core.execution.executor import Executor
from core.exchange.internal_cex import InternalCEX


def test_executor_place_and_close_pair():
    exe = Executor(InternalCEX())
    leg1 = {"symbol": "BTCUSDT_PERP", "side": "BUY", "qty": 1, "price": 100}
    leg2 = {"symbol": "BTCUSDT_SPOT", "side": "SELL", "qty": 1, "price": 100}
    res = exe.place_ioc_pair(leg1, leg2, 800, 35)
    assert res["status"] == "filled"
    pid = res["position_id"]
    assert pid in exe.positions
    closed = exe.close_position(pid)
    assert closed["status"] == "closed"

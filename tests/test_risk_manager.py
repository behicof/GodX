from core.risk.manager import RiskManager


def test_pos_usd_boundary():
    rm = RiskManager()
    ok, _ = rm.check({"qty": 1, "pos_usd": rm.max_pos_usd, "leverage": 1})
    assert ok
    ok, reason = rm.check({"qty": 1, "pos_usd": rm.max_pos_usd + 1, "leverage": 1})
    assert not ok and "pos_usd" in reason


def test_leverage_boundary():
    rm = RiskManager()
    ok, _ = rm.check({"qty": 1, "leverage": rm.max_leverage})
    assert ok
    ok, reason = rm.check({"qty": 1, "leverage": rm.max_leverage + 0.1})
    assert not ok and "leverage" in reason


def test_rejects_non_positive_qty():
    rm = RiskManager()
    ok, reason = rm.check({"qty": 0})
    assert not ok and "quantity" in reason

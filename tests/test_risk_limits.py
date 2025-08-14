from core.risk.manager import RiskManager


def test_risk_manager_accepts_positive_qty_and_rejects_non_positive():
    config = {"max_position": 10}
    rm = RiskManager(config)
    assert rm.check({"qty": 1})
    assert not rm.check({"qty": 0})
    assert not rm.check({"qty": -1})

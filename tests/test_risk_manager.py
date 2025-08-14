from core.risk.manager import RiskManager


def test_risk_manager_accepts_positive_qty_and_rejects_non_positive():
    sample_config = {"max_qty": 100}
    rm = RiskManager()
    assert rm.check({"qty": 5}) is True
    assert rm.check({"qty": 0}) is False
    assert rm.check({"qty": -10}) is False

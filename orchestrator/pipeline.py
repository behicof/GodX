from core.risk.guards import RiskManager
from core.execution.executor import Executor
from core.exchange.base import Exchange


class Pipeline:
    """End-to-end trading pipeline."""

    def __init__(self, exchange: Exchange, risk_cfg: dict | None = None):
        self.risk = RiskManager(risk_cfg or {})
        self.executor = Executor(exchange)

    def run(self, opportunity: dict):
        notional = opportunity.get("notional_usd", opportunity.get("qty", 0) * opportunity.get("price", 0))
        sym_exp = opportunity.get("sym_exposure_usd", 0)
        ex_exp = opportunity.get("ex_exposure_usd", 0)
        ok, reason = self.risk.check(opportunity["symbol"], notional, sym_exp, ex_exp)
        if not ok:
            return {"status": "rejected", "reason": reason}
        return self.executor.execute(
            opportunity["symbol"], opportunity["side"], opportunity["qty"], opportunity.get("price")
        )

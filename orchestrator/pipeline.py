from core.risk.manager import RiskCfg, RiskManager
from core.execution.executor import Executor
from core.exchange.base import Exchange

class Pipeline:
    """End-to-end trading pipeline."""

    def __init__(self, exchange: Exchange, risk_cfg: RiskCfg | dict | None = None):
        self.risk = RiskManager(risk_cfg)
        self.executor = Executor(exchange)

    def run(self, opportunity: dict, sym_exposure_usd: float, ex_exposure_usd: float):
        notional = opportunity.get("notional_usd")
        if notional is None:
            price = opportunity.get("price", 0)
            notional = opportunity.get("qty", 0) * price
        approved, reason = self.risk.check(
            opportunity["symbol"], notional, sym_exposure_usd, ex_exposure_usd
        )
        if not approved:
            return {"status": "rejected", "reason": reason}
        return self.executor.execute(
            opportunity["symbol"], opportunity["side"], opportunity["qty"], opportunity.get("price")
        )

from core.risk.manager import RiskManager
from core.execution.executor import Executor
from core.execution.result import ExecResult
from core.exchange.base import Exchange

class Pipeline:
    """End-to-end trading pipeline."""

    def __init__(self, exchange: Exchange):
        self.risk = RiskManager()
        self.executor = Executor(exchange)

    def run(self, opportunity: dict) -> ExecResult:
        if not self.risk.check(opportunity):
            return ExecResult(ok=False, reason="rejected")

        leg1 = {
            "symbol": opportunity["symbol"],
            "side": opportunity["side"],
            "quantity": opportunity["qty"],
            "price": opportunity.get("price"),
        }
        leg2_data = opportunity.get("leg2")
        leg2 = None
        if leg2_data:
            leg2 = {
                "symbol": leg2_data["symbol"],
                "side": leg2_data["side"],
                "quantity": leg2_data["qty"],
                "price": leg2_data.get("price"),
            }
        return self.executor.execute(leg1, leg2)

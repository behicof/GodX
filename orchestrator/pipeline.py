from core.risk.manager import RiskManager
from core.execution.executor import Executor
from core.exchange.base import Exchange

class Pipeline:
    """End-to-end trading pipeline."""

    def __init__(self, exchange: Exchange):
        self.risk = RiskManager()
        self.executor = Executor(exchange)

    def run(self, opportunity: dict):
        if not self.risk.check(opportunity):
            return {"status": "rejected"}
        return self.executor.execute(
            opportunity["symbol"], opportunity["side"], opportunity["qty"], opportunity.get("price")
        )

from core.risk.manager import RiskManager
from core.execution.executor import Executor
from core.execution.types import ExecResult
from core.exchange.base import Exchange

class Pipeline:
    """End-to-end trading pipeline."""

    def __init__(self, exchange: Exchange, max_latency_ms: int = 1000):
        self.risk = RiskManager()
        self.executor = Executor(exchange, max_latency_ms)

    def run(self, opportunity: dict) -> ExecResult:
        if not self.risk.check(opportunity):
            return ExecResult(False, "risk_rejected")
        leg1, leg2 = opportunity["legs"]
        return self.executor.execute_pair(leg1, leg2)

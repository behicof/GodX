from dataclasses import dataclass

from core.risk.manager import RiskManager
from core.execution.executor import Executor
from core.exchange.base import Exchange
from core.data.logger import logger


@dataclass
class ExecutionResult:
    """Structured result of pipeline execution."""

    status: str
    details: dict
    opportunity: dict

class Pipeline:
    """End-to-end trading pipeline."""

    def __init__(self, exchange: Exchange):
        self.risk = RiskManager()
        self.executor = Executor(exchange)

    def run(self, opportunity: dict) -> ExecutionResult:
        if not self.risk.check(opportunity):
            logger.info(f"rejected_opportunity {opportunity}")
            return ExecutionResult(
                status="rejected",
                details={"reason": "risk_check_failed"},
                opportunity=opportunity,
            )

        logger.info(f"accepted_opportunity {opportunity}")
        details = self.executor.execute(
            opportunity["symbol"],
            opportunity["side"],
            opportunity["qty"],
            opportunity.get("price"),
        )
        return ExecutionResult(
            status=details.get("status", "unknown"),
            details=details,
            opportunity=opportunity,
        )

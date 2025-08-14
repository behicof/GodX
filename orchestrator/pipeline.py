from dataclasses import dataclass
from typing import Optional

from core.risk.manager import RiskManager
from core.execution.executor import Executor
from core.exchange.base import Exchange
from core.data.logger import logger


@dataclass
class PipelineResult:
    """Typed result of a pipeline run."""

    accepted: bool
    reason: str
    execution: Optional[dict] = None


class Pipeline:
    """End-to-end trading pipeline."""

    def __init__(self, exchange: Exchange):
        self.risk = RiskManager()
        self.executor = Executor(exchange)

    def run(self, opportunity: dict) -> PipelineResult:
        if not self.risk.check(opportunity):
            logger.info("rejected")
            return PipelineResult(False, "rejected")

        try:
            execution = self.executor.execute(
                opportunity["symbol"],
                opportunity["side"],
                opportunity["qty"],
                opportunity.get("price"),
            )
            return PipelineResult(True, "accepted", execution)
        except Exception:
            logger.exception("exec_fail")
            return PipelineResult(False, "exec_fail")

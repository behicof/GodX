from dataclasses import dataclass
from time import perf_counter

from core.risk.manager import RiskManager
from core.execution.executor import Executor
from core.exchange.base import Exchange
from core.data.logger import logger


@dataclass
class PipelineResult:
    """Result container for pipeline operations."""

    accepted: bool
    reason: str
    exec: dict | None = None

class Pipeline:
    """End-to-end trading pipeline."""

    def __init__(self, exchange: Exchange):
        self.risk = RiskManager()
        self.executor = Executor(exchange)

    def run(self, opportunity: dict) -> PipelineResult:
        start = perf_counter()
        symbol = opportunity.get("symbol", "")

        if not self.risk.check(opportunity):
            latency = perf_counter() - start
            logger.info(f"rejected symbol={symbol} latency={latency:.6f}")
            return PipelineResult(False, "rejected")

        try:
            exec_details = self.executor.execute(
                opportunity["symbol"],
                opportunity["side"],
                opportunity["qty"],
                opportunity.get("price"),
            )
            return PipelineResult(True, "accepted", exec_details)
        except Exception:
            latency = perf_counter() - start
            logger.error(f"exec_fail symbol={symbol} latency={latency:.6f}")
            return PipelineResult(False, "exec_fail")

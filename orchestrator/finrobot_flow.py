"""Orchestrator wiring the agent flow."""

from __future__ import annotations

from typing import Dict

from core.execution import funding_arb
from core.execution.executor import Executor
from core.exchange.internal_cex import InternalCEX
from core.data.logger import logger
from nlp.fingpt_hooks import summarize_news


class Orchestrator:
    """Simplified orchestrator with run hooks."""

    def __init__(self, cfg: Dict[str, dict]):
        self.cfg = cfg
        self.executor = Executor(InternalCEX())

    def run_once(self) -> None:
        """Run a single scan/execute cycle."""
        quotes = {"BTCUSDT": {"bid": 100, "ask": 101}}
        funding = {"BTCUSDT": 500}
        opps = funding_arb.scan_opportunities(quotes, funding, self.cfg["thresholds"]["funding_arb"])
        if not opps:
            logger.info("no_opportunity")
            return
        opp = opps[0]
        res = funding_arb.execute(opp, self.executor, {**self.cfg["risk"], **self.cfg["thresholds"]["funding_arb"]})
        logger.info(f"execution_result={res}")
        summarize_news("dummy")

    def run_forever(self) -> None:
        while True:
            self.run_once()
            break

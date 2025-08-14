import time
from core.exchange.base import Exchange
from core.data.logger import logger
from core.execution.types import ExecResult


class Executor:
    """Trade executor handling two-leg strategies."""

    def __init__(self, exchange: Exchange, max_latency_ms: int = 1000):
        self.exchange = exchange
        self.max_latency_ms = max_latency_ms

    def execute_pair(self, leg1: dict, leg2: dict) -> ExecResult:
        details = {"latency_ms": {}, "responses": {}, "max_latency_ms": self.max_latency_ms}
        # First leg
        try:
            start = time.perf_counter()
            resp1 = self.exchange.place_order_ioc(
                leg1["symbol"], leg1["side"], leg1["qty"], leg1.get("price")
            )
            latency1 = (time.perf_counter() - start) * 1000
            details["latency_ms"]["leg1"] = latency1
            details["responses"]["leg1"] = resp1
            if latency1 > self.max_latency_ms:
                logger.warning(f"Leg1 latency {latency1:.2f}ms exceeds {self.max_latency_ms}ms")
        except Exception as e:
            logger.exception("First leg failed")
            details["error"] = str(e)
            return ExecResult(False, "first_leg_failed", details)

        # Second leg
        try:
            start = time.perf_counter()
            resp2 = self.exchange.place_order_ioc(
                leg2["symbol"], leg2["side"], leg2["qty"], leg2.get("price")
            )
            latency2 = (time.perf_counter() - start) * 1000
            details["latency_ms"]["leg2"] = latency2
            details["responses"]["leg2"] = resp2
            if latency2 > self.max_latency_ms:
                logger.warning(f"Leg2 latency {latency2:.2f}ms exceeds {self.max_latency_ms}ms")
        except Exception as e:
            logger.exception("Second leg failed")
            details["error"] = str(e)
            # Attempt rollback
            rollback_side = "SELL" if leg1["side"].upper() == "BUY" else "BUY"
            try:
                self.exchange.place_order_ioc(
                    leg1["symbol"], rollback_side, leg1["qty"], leg1.get("price")
                )
            except Exception as re:
                logger.exception("Rollback failed")
                details["rollback_error"] = str(re)
            return ExecResult(False, "second_leg_failed", details)

        return ExecResult(True, details=details)

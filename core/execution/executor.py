import time

from core.exchange.base import Exchange
from core.data.logger import logger
from core.execution.result import ExecResult
from core.execution.utils import suppress_exc


class Executor:
    """Simple trade executor handling multi-leg IOC orders."""

    def __init__(self, exchange: Exchange, max_latency_ms: float = 250.0):
        self.exchange = exchange
        self.max_latency_ms = max_latency_ms

    def execute(self, leg1: dict, leg2: dict | None = None) -> ExecResult:
        start = time.perf_counter()
        try:
            logger.info(
                f"leg1 symbol={leg1['symbol']} side={leg1['side']} qty={leg1['quantity']} price={leg1.get('price')}"
            )
            details1 = self.exchange.place_order(**leg1)
        except Exception as exc:
            logger.exception("leg1 order failed")
            latency = (time.perf_counter() - start) * 1000
            return ExecResult(False, f"leg1 error: {exc}", latency_ms=latency)

        details = {"leg1": details1}
        if leg2 is not None:
            try:
                logger.info(
                    f"leg2 symbol={leg2['symbol']} side={leg2['side']} qty={leg2['quantity']} price={leg2.get('price')}"
                )
                details2 = self.exchange.place_order(**leg2)
                details["leg2"] = details2
            except Exception as exc:
                logger.exception("leg2 order failed")
                with suppress_exc():
                    rollback_side = "SELL" if leg1["side"].upper() == "BUY" else "BUY"
                    self.exchange.place_order(
                        symbol=leg1["symbol"],
                        side=rollback_side,
                        quantity=leg1["quantity"],
                        price=leg1.get("price"),
                    )
                latency = (time.perf_counter() - start) * 1000
                return ExecResult(False, f"leg2 error: {exc}", details, latency)

        latency = (time.perf_counter() - start) * 1000
        if latency > self.max_latency_ms:
            logger.warning(
                f"latency {latency:.2f}ms exceeds {self.max_latency_ms}ms"
            )
        return ExecResult(True, "ok", details, latency)

from core.exchange.base import Exchange
from core.data.logger import logger
from libs.metrics import counter, gauge
import time

class Executor:
    """Simple trade executor."""

    def __init__(self, exchange: Exchange):
        self.exchange = exchange

    execute_latency = gauge(
        "executor_execute_latency_seconds", "Latency of execute() calls"
    )
    execute_errors = counter(
        "executor_execute_errors_total", "Total errors during execute()"
    )

    def execute(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict:
        start = time.perf_counter()
        try:
            logger.info(
                f"execute_order symbol={symbol} side={side} qty={quantity} price={price}"
            )
            return self.exchange.place_order(symbol, side, quantity, price)
        except Exception:
            self.execute_errors.inc()
            raise
        finally:
            self.execute_latency.set(time.perf_counter() - start)

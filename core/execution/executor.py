from core.exchange.base import Exchange
from core.data.logger import logger
import time


class Executor:
    """Simple trade executor with basic retry handling."""

    def __init__(self, exchange: Exchange, retries: int = 0, retry_delay: float = 0.0):
        self.exchange = exchange
        self.retries = retries
        self.retry_delay = retry_delay

    def execute(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict:
        logger.info(
            f"execute_order symbol={symbol} side={side} qty={quantity} price={price}"
        )
        attempt = 0
        while True:
            try:
                return self.exchange.place_order(symbol, side, quantity, price)
            except Exception as e:  # broad catch to surface any order issues
                logger.error(f"place_order failed: {e}")
                if attempt >= self.retries:
                    return {"status": "error", "detail": str(e)}
                attempt += 1
                if self.retry_delay:
                    time.sleep(self.retry_delay)
                logger.info(f"retrying order, attempt {attempt}")

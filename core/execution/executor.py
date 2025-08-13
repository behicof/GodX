from core.exchange.base import Exchange
from core.data.logger import logger

class Executor:
    """Simple trade executor."""

    def __init__(self, exchange: Exchange):
        self.exchange = exchange

    def execute(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict:
        logger.info(f"execute_order symbol={symbol} side={side} qty={quantity} price={price}")
        return self.exchange.place_order(symbol, side, quantity, price)

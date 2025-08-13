"""Internal mock exchange for testing."""

from __future__ import annotations

from typing import Dict

from .base import Exchange


class InternalCEX(Exchange):
    """Very small in-memory exchange."""

    def __init__(self):
        self.last_price = {}

    def place_order(self, symbol: str, side: str, qty: float, price: float | None = None) -> Dict[str, float]:
        self.last_price[symbol] = price
        return {"symbol": symbol, "side": side, "qty": qty, "price": price, "status": "filled"}

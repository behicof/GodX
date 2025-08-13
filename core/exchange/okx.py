"""OKX exchange stub."""

from __future__ import annotations

from typing import Dict

from .base import Exchange


class OKX(Exchange):
    def place_order(self, symbol: str, side: str, qty: float, price: float | None = None) -> Dict[str, float]:
        return {"symbol": symbol, "side": side, "qty": qty, "price": price}

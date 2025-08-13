"""Trade execution utilities."""

from __future__ import annotations

from typing import Dict, Any

from core.exchange.base import Exchange
from core.data.logger import logger


class Executor:
    """Simple in-memory executor for testing."""

    def __init__(self, exchange: Exchange):
        self.exchange = exchange
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.balances: Dict[str, float] = {"USD": 1_000_000.0}

    def place_ioc_pair(self, leg1: Dict[str, Any], leg2: Dict[str, Any], max_latency_ms: int, max_slippage_bps: int) -> Dict[str, Any]:
        """Place two IOC orders representing an arbitrage pair."""
        res1 = self.exchange.place_order(leg1["symbol"], leg1["side"], leg1["qty"], leg1.get("price"))
        res2 = self.exchange.place_order(leg2["symbol"], leg2["side"], leg2["qty"], leg2.get("price"))
        pos_id = f"pos-{len(self.positions)+1}"
        self.positions[pos_id] = {"legs": [res1, res2]}
        self.balances["USD"] -= leg1.get("qty", 0) * (leg1.get("price") or 0)
        logger.info(f"executed_pair id={pos_id}")
        return {"position_id": pos_id, "legs": [res1, res2], "status": "filled"}

    def close_position(self, position_id: str) -> Dict[str, Any]:
        pos = self.positions.pop(position_id, None)
        if pos:
            logger.info(f"close_position id={position_id}")
            return {"status": "closed", "position_id": position_id}
        return {"status": "not_found", "position_id": position_id}

    def get_balances(self) -> Dict[str, float]:
        return dict(self.balances)

"""Position sizing helpers."""

from __future__ import annotations

from typing import Dict


def size_position(symbol: str, net_edge_bps: int, risk_cfg: Dict[str, float], balances: Dict[str, float]) -> float:
    """Compute a position size based on net edge and risk constraints."""
    max_notional = risk_cfg.get("max_notional_per_trade_usd", 0)
    usd_balance = balances.get("USD", 0)
    base = min(max_notional, usd_balance)
    multiplier = max(min(net_edge_bps / 1000, 1), 0.1)
    return base * multiplier / 1000

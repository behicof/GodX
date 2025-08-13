"""Risk guard utilities."""

from __future__ import annotations

from typing import Dict


def check_slippage(book: Dict[str, float], max_bps: int) -> bool:
    """Validate executed slippage against a threshold in basis points."""
    expected = book.get("expected", 0)
    price = book.get("price", expected)
    if expected == 0:
        return True
    slippage_bps = abs(price - expected) / expected * 10000
    return slippage_bps <= max_bps


def check_latency(latency_ms: int, max_latency_ms: int) -> bool:
    """Check that observed latency is within bound."""
    return latency_ms <= max_latency_ms


def check_depth(book: Dict[str, float], min_depth: float) -> bool:
    """Ensure orderbook has sufficient USD depth."""
    return book.get("depth", 0.0) >= min_depth


def check_liquidation(sym: str, buf: float) -> bool:
    """Dummy liquidation distance check always passing."""
    return buf > 0

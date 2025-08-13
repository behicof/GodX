"""Funding rate arbitrage execution logic."""

from __future__ import annotations

from typing import Dict, List

from core.risk import sizing
from core.risk import guards


def scan_opportunities(quotes: Dict[str, Dict[str, float]], funding_info: Dict[str, float], cfg: Dict[str, int]) -> List[Dict[str, float]]:
    """Scan quotes and funding data for viable opportunities."""
    opportunities: List[Dict[str, float]] = []
    threshold = cfg.get("min_net_edge_bps", 0)
    for sym, rate_bps in funding_info.items():
        net_edge = rate_bps - cfg.get("fees_bps", 0)
        if net_edge >= threshold:
            opportunities.append({"symbol": sym, "net_edge_bps": net_edge})
    return opportunities


def execute(opportunity: Dict[str, float], exe, risk_cfg: Dict[str, float]) -> Dict[str, object]:
    """Execute a funding arbitrage opportunity."""
    symbol = opportunity["symbol"]
    qty = sizing.size_position(symbol, opportunity["net_edge_bps"], risk_cfg, exe.get_balances())
    leg1 = {"symbol": f"{symbol}_PERP", "side": "BUY", "qty": qty, "price": opportunity.get("perp_price", 0), "latency_ms": 10, "book": {"expected": opportunity.get("perp_price", 0), "price": opportunity.get("perp_price", 0), "depth": 1e6}}
    leg2 = {"symbol": f"{symbol}_SPOT", "side": "SELL", "qty": qty, "price": opportunity.get("spot_price", 0), "latency_ms": 10, "book": {"expected": opportunity.get("spot_price", 0), "price": opportunity.get("spot_price", 0), "depth": 1e6}}
    if not guards.check_latency(leg1["latency_ms"], risk_cfg.get("max_leg_latency_ms", 1000)):
        return {"status": "rejected", "reason": "latency"}
    if not guards.check_slippage(leg1["book"], risk_cfg.get("max_slippage_bps", 100)):
        return {"status": "rejected", "reason": "slippage"}
    res = exe.place_ioc_pair(leg1, leg2, risk_cfg.get("max_leg_latency_ms", 1000), risk_cfg.get("max_slippage_bps", 100))
    return res

"""Cross-exchange arbitrage module stub."""

from __future__ import annotations

from typing import Dict


def scan_opportunities(orderbooks: Dict[str, Dict[str, float]], cfg: Dict[str, float]) -> list[Dict[str, float]]:
    """Placeholder for cross-exchange scan."""
    return []


def execute(opportunity: Dict[str, float], exe, risk_cfg: Dict[str, float]) -> Dict[str, object]:
    """Placeholder execute returning rejected status."""
    return {"status": "not_implemented"}

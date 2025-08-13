"""Cash-and-carry arbitrage module stub."""

from __future__ import annotations

from typing import Dict


def scan_opportunities(data: Dict[str, float], cfg: Dict[str, float]) -> list[Dict[str, float]]:
    """Placeholder for basis scan implementation."""
    return []


def execute(opportunity: Dict[str, float], exe, risk_cfg: Dict[str, float]) -> Dict[str, object]:
    """Placeholder execute returning rejected status."""
    return {"status": "not_implemented"}

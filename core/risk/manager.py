from __future__ import annotations

from pathlib import Path
from typing import Tuple

import yaml


class RiskManager:
    """Very small placeholder risk manager."""

    def __init__(self) -> None:
        cfg_path = Path(__file__).resolve().parents[2] / "config" / "risk.yml"
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        self.max_pos_usd = cfg.get("max_pos_usd", float("inf"))
        self.max_leverage = cfg.get("max_leverage", float("inf"))

    def check(self, opportunity: dict) -> Tuple[bool, str]:
        """Validate opportunity against basic risk checks."""
        qty = opportunity.get("qty", 0)
        if qty <= 0:
            return False, "non-positive quantity"

        pos_usd = opportunity.get("pos_usd", 0)
        if pos_usd > self.max_pos_usd:
            return False, f"pos_usd {pos_usd} exceeds max {self.max_pos_usd}"

        leverage = opportunity.get("leverage", 0)
        if leverage > self.max_leverage:
            return False, f"leverage {leverage} exceeds max {self.max_leverage}"

        return True, "approved"

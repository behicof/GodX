"""Risk adjustment stub using RAG/LLM signals."""

from __future__ import annotations

from typing import Dict


def risk_adjust(signals: Dict[str, float]) -> float:
    """Compute risk multiplier in [0.3, 1.5]."""
    mult = signals.get("risk_multiplier", 1.0)
    return max(0.3, min(1.5, mult))


if __name__ == "__main__":
    risk_adjust({})

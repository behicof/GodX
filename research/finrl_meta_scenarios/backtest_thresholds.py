"""Backtesting thresholds stub."""

from __future__ import annotations

from typing import Dict, List


def run_backtest(data: List[Dict[str, float]], grid: Dict[str, List[int]]) -> Dict[str, float]:
    """Return fake metrics for given grid search."""
    return {"hit_rate": 0.0, "avg_net_edge": 0.0}


if __name__ == "__main__":
    run_backtest([], {})

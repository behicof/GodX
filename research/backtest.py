"""Backtesting utilities.

This module provides a simple backtesting engine that operates on a
price series and a user supplied strategy.  It exposes both a Python
API via :func:`run` and a CLI that can be invoked with ``python -m
research.backtest`` to run the backtest against data stored in CSV or
Parquet files.
"""

from __future__ import annotations

import argparse
from math import sqrt
from pathlib import Path
from typing import Callable, Dict

import pandas as pd


def run(price_series: pd.Series, strategy: Callable[[pd.Series], pd.Series]) -> Dict[str, float]:
    """Execute a simple backtest.

    Parameters
    ----------
    price_series:
        Series of asset prices ordered by time.
    strategy:
        Callable that accepts the ``price_series`` and returns a series of
        positions (e.g. ``1`` for long, ``-1`` for short) indexed the same
        way as ``price_series``.

    Returns
    -------
    dict
        Dictionary containing ``cumulative_pnl``, ``sharpe_ratio`` and
        ``max_drawdown``.
    """

    prices = price_series.astype(float)
    positions = strategy(prices).reindex(prices.index).astype(float)

    returns = prices.pct_change().fillna(0.0)
    pnl = positions.shift(1).fillna(0.0) * returns
    cumulative = pnl.cumsum()

    mean = pnl.mean()
    std = pnl.std(ddof=0)
    sharpe = (mean / std * sqrt(len(pnl))) if std != 0 else 0.0

    drawdown = cumulative - cumulative.cummax()
    max_drawdown = drawdown.min() if not drawdown.empty else 0.0

    return {
        "cumulative_pnl": float(cumulative.iloc[-1]) if not cumulative.empty else 0.0,
        "sharpe_ratio": float(sharpe),
        "max_drawdown": float(max_drawdown),
    }


def _load_prices(path: Path, column: str) -> pd.Series:
    """Load a price series from a CSV or Parquet file."""

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in {".parquet", ".pq"}:
        df = pd.read_parquet(path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in data file")
    return df[column]


def _buy_and_hold(prices: pd.Series) -> pd.Series:
    """Trivial strategy that is always long one unit."""

    return pd.Series(1.0, index=prices.index)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a simple backtest over price data")
    parser.add_argument("data", type=str, help="Path to CSV or Parquet file containing prices")
    parser.add_argument("--column", default="close", help="Column name containing prices")
    parser.add_argument(
        "--strategy",
        default="buy_and_hold",
        choices=["buy_and_hold"],
        help="Strategy to execute",
    )
    args = parser.parse_args()

    prices = _load_prices(Path(args.data), args.column)
    strategies = {"buy_and_hold": _buy_and_hold}
    metrics = run(prices, strategies[args.strategy])
    for k, v in metrics.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()


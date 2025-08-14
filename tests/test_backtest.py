import pandas as pd
import pytest

from research.backtest import run


def always_long(prices: pd.Series) -> pd.Series:
    """Return a constant long position."""

    return pd.Series(1.0, index=prices.index)


def test_backtest_metrics():
    prices = pd.Series([1, 2, 1, 2])
    metrics = run(prices, always_long)

    assert metrics["cumulative_pnl"] == pytest.approx(1.5)
    assert metrics["sharpe_ratio"] == pytest.approx(1.1547, rel=1e-3)
    assert metrics["max_drawdown"] == pytest.approx(-0.5)


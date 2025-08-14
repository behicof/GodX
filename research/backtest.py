"""Basic backtesting utilities for basis trading.

This module implements a minimalistic backtester for a simple basis
trading strategy.  It assumes the input OHLCV :class:`pandas.DataFrame`
contains both spot and perpetual price series.  If either series is
missing the single ``close`` column is used for both legs.  The strategy
enters a *short basis* position when the perpetual trades above the spot
by ``entry_bps`` and a *long basis* when the reverse occurs.  Positions
are closed when the basis crosses back through zero.

Fees and slippage (``fee_bps`` and ``slip_bps``) are charged on each leg
whenever a trade is executed.  Latency is modelled only implicitly via
the data frequency and ``latency_ms`` configuration value, i.e. orders
are filled on the next bar.  The simulation reports total PnL, number of
trades, Sharpe ratio and maximum drawdown.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class BTConfig:
    """Configuration for the basis trading backtest.

    Attributes
    ----------
    fee_bps:
        Fee paid per trade leg in basis points.
    slip_bps:
        Slippage per trade leg in basis points.
    latency_ms:
        Order execution latency in milliseconds.
    entry_bps:
        Entry threshold for the basis in basis points.
    """

    fee_bps: float = 0.0
    slip_bps: float = 0.0
    latency_ms: int = 0
    entry_bps: float = 0.0


def simulate_basis(df: pd.DataFrame, cfg: BTConfig) -> dict:
    """Simulate a simple basis trading strategy.

    Parameters
    ----------
    df:
        OHLCV data.  Should contain ``spot`` and ``perp`` price columns;
        if missing, a single ``close`` column is used for both.
    cfg:
        Backtest configuration.

    Returns
    -------
    dict
        Dictionary with keys ``pnl``, ``trades``, ``sharpe`` and
        ``max_drawdown``.
    """

    # Select price series
    spot = (
        df["spot"]
        if "spot" in df
        else df.get("spot_close", df.get("close"))
    )
    perp = (
        df["perp"]
        if "perp" in df
        else df.get("perp_close", df.get("close"))
    )

    if spot is None or perp is None:
        raise ValueError("DataFrame must contain price data")

    basis = (perp - spot) / spot
    basis_diff = basis.diff().fillna(0)

    entry = cfg.entry_bps / 10_000.0
    cost = (cfg.fee_bps + cfg.slip_bps) / 10_000.0

    position = 0
    positions = []
    trades = 0

    for b in basis:
        if position == 0:
            if b > entry:
                position = -1
                trades += 1
            elif b < -entry:
                position = 1
                trades += 1
        elif position == 1 and b >= 0:
            position = 0
            trades += 1
        elif position == -1 and b <= 0:
            position = 0
            trades += 1
        positions.append(position)

    pos = pd.Series(positions, index=df.index)

    returns = pos.shift(1).fillna(0) * basis_diff
    fees = abs(pos.diff().fillna(0)) * cost
    pnl_series = returns - fees
    cum_pnl = pnl_series.cumsum()

    sharpe = 0.0
    if pnl_series.std() > 0:
        sharpe = pnl_series.mean() / pnl_series.std() * np.sqrt(len(pnl_series))

    running_max = cum_pnl.cummax()
    drawdown = running_max - cum_pnl
    max_dd = float(drawdown.max())

    return {
        "pnl": float(cum_pnl.iat[-1]),
        "trades": int(trades),
        "sharpe": float(sharpe),
        "max_drawdown": max_dd,
    }


def run():
    """Backward compatibility placeholder returning zero PnL."""

    return {"pnl": 0}

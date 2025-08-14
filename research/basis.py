from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd


@dataclass
class BTConfig:
    """Backtest configuration.

    Attributes
    ----------
    fee: float
        Fractional fee applied to each leg of the trade.
    slippage: float
        Fractional slippage per leg.
    latency: int
        Number of rows to delay execution after a signal.
    long_entry: float
        Basis threshold for entering a long basis trade
        (long future / short spot).
    short_entry: float
        Basis threshold for entering a short basis trade
        (short future / long spot).
    """

    fee: float = 0.0
    slippage: float = 0.0
    latency: int = 0
    long_entry: float = 0.0
    short_entry: float = 0.0


def simulate_basis(df: pd.DataFrame, cfg: BTConfig) -> Dict[str, float]:
    """Simulate a simple basis-trading strategy.

    Parameters
    ----------
    df:
        DataFrame with at least ``spot`` and ``future`` price columns sorted by
        time. Example CSV/Parquet structure::

            timestamp,spot,future
            2024-01-01T00:00:00Z,100,105
            2024-01-01T00:01:00Z,101,104

    cfg:
        Backtest configuration.

    Returns
    -------
    dict
        Dictionary with ``pnl``, ``trades``, ``sharpe`` and ``max_drawdown``.

    Notes
    -----
    - Uses one unit of notional per leg.
    - Fees and slippage apply to each of the four legs (open/close spot & future).
    - ``latency`` delays execution by N rows after a signal is generated.
    - Entries occur when basis ``> cfg.short_entry`` (short basis) or
      ``< -cfg.long_entry`` (long basis) and exit when basis crosses zero.
    """

    if not {"spot", "future"}.issubset(df.columns):
        raise ValueError("df must contain 'spot' and 'future' columns")

    data = df.reset_index(drop=True).copy()
    data["basis"] = (data["future"] - data["spot"]) / data["spot"]

    trades = []
    position = 0  # 1 = long basis, -1 = short basis
    entry_spot = entry_future = 0.0

    for i in range(len(data) - cfg.latency):
        spot_price = data.at[i + cfg.latency, "spot"]
        future_price = data.at[i + cfg.latency, "future"]
        basis = data.at[i, "basis"]

        if position == 0:
            if basis > cfg.short_entry:
                position = -1
                entry_spot = spot_price
                entry_future = future_price
            elif basis < -cfg.long_entry:
                position = 1
                entry_spot = spot_price
                entry_future = future_price
        elif position == -1 and basis <= 0:
            exit_spot = spot_price
            exit_future = future_price
            pnl = (entry_future - exit_future) + (exit_spot - entry_spot)
            cost = (cfg.fee + cfg.slippage) * (
                entry_future + entry_spot + exit_future + exit_spot
            )
            trades.append(pnl - cost)
            position = 0
        elif position == 1 and basis >= 0:
            exit_spot = spot_price
            exit_future = future_price
            pnl = (exit_future - entry_future) - (exit_spot - entry_spot)
            cost = (cfg.fee + cfg.slippage) * (
                entry_future + entry_spot + exit_future + exit_spot
            )
            trades.append(pnl - cost)
            position = 0

    pnl = float(np.sum(trades))
    n_trades = len(trades)
    if n_trades > 1 and np.std(trades) != 0:
        sharpe = float(np.mean(trades) / np.std(trades) * np.sqrt(n_trades))
    else:
        sharpe = 0.0

    if n_trades:
        equity = np.cumsum(trades)
        running_max = np.maximum.accumulate(equity)
        max_drawdown = float(np.max(running_max - equity))
    else:
        max_drawdown = 0.0

    return {
        "pnl": pnl,
        "trades": n_trades,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
    }

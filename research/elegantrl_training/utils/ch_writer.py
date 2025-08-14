"""Utilities to fetch OHLCV data from ClickHouse and persist engineered features to parquet."""

from __future__ import annotations

from pathlib import Path
from typing import Optional
import os
import pandas as pd


def _get_client(url: Optional[str] = None):
    """Create a ClickHouse client.

    Parameters
    ----------
    url : str, optional
        Connection URL. If not provided, ``CLICKHOUSE_URL`` env var or
        ``clickhouse://default:@localhost:9000`` is used.
    """
    from clickhouse_driver import Client

    url = url or os.getenv("CLICKHOUSE_URL", "clickhouse://default:@localhost:9000")
    return Client.from_url(url)


def fetch_ohlcv(symbol: str, start: str, end: str, client=None) -> pd.DataFrame:
    """Fetch OHLCV data for ``symbol`` between ``start`` and ``end``.

    Parameters
    ----------
    symbol : str
        Market symbol identifier, e.g. ``BTCUSDT``.
    start : str
        Inclusive start timestamp.
    end : str
        Inclusive end timestamp.
    client : clickhouse_driver.Client, optional
        Existing client instance. If ``None`` a client will be created.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns ``timestamp, open, high, low, close, volume``.
    """
    if client is None:
        client = _get_client()

    query = (
        """
        SELECT timestamp, open, high, low, close, volume
        FROM ohlcv
        WHERE symbol = %(symbol)s AND timestamp BETWEEN %(start)s AND %(end)s
        ORDER BY timestamp
        """
    )
    data = client.execute(query, {"symbol": symbol, "start": start, "end": end})
    return pd.DataFrame(
        data, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute technical indicators on an OHLCV DataFrame.

    Adds columns ``hl2``, ``vol``, ``rsi14``, ``std20`` and ``zscore``.
    """
    df = df.copy()
    df["hl2"] = (df["high"] + df["low"]) / 2
    df["vol"] = df["volume"]

    # RSI-14
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
    rs = avg_gain / avg_loss
    df["rsi14"] = 100 - (100 / (1 + rs))

    rolling_std = df["close"].rolling(window=20)
    df["std20"] = rolling_std.std()
    rolling_mean = df["close"].rolling(window=20).mean()
    df["zscore"] = (df["close"] - rolling_mean) / df["std20"]

    return df


def write_parquet(symbol: str, start: str, end: str, out_dir: str = "data/parquet") -> Path:
    """Fetch OHLCV data, engineer features and persist to parquet.

    Parameters
    ----------
    symbol : str
        Market symbol identifier.
    start : str
        Inclusive start timestamp.
    end : str
        Inclusive end timestamp.
    out_dir : str, default ``"data/parquet"``
        Base output directory.

    Returns
    -------
    pathlib.Path
        Path to the written parquet file.
    """
    df = compute_features(fetch_ohlcv(symbol, start, end))

    safe_start = start.replace(":", "").replace(" ", "_")
    safe_end = end.replace(":", "").replace(" ", "_")
    output_path = Path(out_dir) / symbol
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / f"{safe_start}_{safe_end}.parquet"
    df.to_parquet(file_path, index=False)
    return file_path

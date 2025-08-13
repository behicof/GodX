"""FinGPT hook stubs."""

from __future__ import annotations


def summarize_news(text: str) -> str:
    """Return a tiny summary."""
    return text[:50]


def explain_trade(trade: dict) -> str:
    """Return a dummy explanation for a trade."""
    return f"explained {trade}"


def weekly_pnl_report(trades: list[dict]) -> str:
    """Return a dummy PnL report."""
    return f"total_trades={len(trades)}"

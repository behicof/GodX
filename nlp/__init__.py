"""NLP modules."""

from .fingpt_hooks import summarize_news, explain_trade, weekly_pnl_report
from .finrag_pipe import get_risk_signals

__all__ = [
    "summarize_news",
    "explain_trade",
    "weekly_pnl_report",
    "get_risk_signals",
]

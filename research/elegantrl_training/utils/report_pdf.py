"""Utility to compile training metrics into a PDF report.

This module reads ``learning.jsonl`` and ``summary.json`` from a given
artifacts directory and assembles plots plus key statistics into a single
``report.pdf``. It is useful for quickly reviewing Elegantrl training runs.

Example
-------
>>> from research.elegantrl_training.utils.report_pdf import generate_report
>>> generate_report("/tmp/experiment")
PosixPath('/tmp/experiment/report.pdf')
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # use non-GUI backend suitable for PDFs
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

__all__ = ["generate_report"]

def _extract(record: dict, keys: list[str]) -> float | None:
    """Return the first value found in ``record`` for any of ``keys``."""
    for key in keys:
        if key in record:
            return record[key]
    return None

def _read_learning_metrics(path: Path) -> tuple[list[float], list[float], list[float]]:
    """Parse ``learning.jsonl`` collecting Sharpe, max drawdown and PnL curves."""
    sharpes: list[float] = []
    drawdowns: list[float] = []
    pnls: list[float] = []

    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            s = _extract(record, ["sharpe", "sharpe_ratio"])
            d = _extract(record, ["max_drawdown", "mdd"])
            p = _extract(record, ["pnl", "profit", "net_profit"])
            if s is not None:
                sharpes.append(s)
            if d is not None:
                drawdowns.append(d)
            if p is not None:
                pnls.append(p)
    return sharpes, drawdowns, pnls

def generate_report(artifacts_dir: str | Path) -> Path:
    """Generate a PDF report from Elegantrl training artifacts.

    Parameters
    ----------
    artifacts_dir:
        Directory containing ``learning.jsonl`` and ``summary.json`` files.

    Returns
    -------
    Path
        Location of the generated ``report.pdf``.
    """
    artifacts = Path(artifacts_dir)
    learning_path = artifacts / "learning.jsonl"
    summary_path = artifacts / "summary.json"
    pdf_path = artifacts / "report.pdf"

    sharpes, drawdowns, pnls = _read_learning_metrics(learning_path)
    summary = {}
    if summary_path.exists():
        with summary_path.open() as f:
            summary = json.load(f)

    with PdfPages(pdf_path) as pdf:
        fig, axes = plt.subplots(3, 1, figsize=(8.27, 11.69))
        axes[0].plot(sharpes)
        axes[0].set_title("Sharpe Ratio")
        axes[1].plot(drawdowns)
        axes[1].set_title("Max Drawdown")
        axes[2].plot(pnls)
        axes[2].set_title("PnL")
        for ax in axes:
            ax.set_xlabel("Step")
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        summary_fig = plt.figure(figsize=(8.27, 11.69))
        summary_fig.axis("off")
        summary_fig.text(0.5, 0.95, "Summary", ha="center", va="top", fontsize=16)
        if summary:
            text = "\n".join(f"{k}: {v}" for k, v in summary.items())
        else:
            text = "No summary statistics available."
        summary_fig.text(0.1, 0.85, text, ha="left", va="top", fontsize=12, family="monospace")
        pdf.savefig(summary_fig)
        plt.close(summary_fig)

    return pdf_path

"""PPO training script stub."""

from __future__ import annotations


def train(symbol: str, epochs: int = 1) -> str:
    """Return path to saved model."""
    return f"ppo_{symbol}.pt"


if __name__ == "__main__":
    train("BTCUSDT")

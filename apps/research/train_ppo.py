"""Placeholder PPO training script."""

import argparse
import pandas as pd

from finrl_meta.envs.market_env import make_env


def train(symbol: str, epochs: int) -> None:
    """Instantiate the market environment and run a dummy training loop."""
    # In practice the dataframe would be loaded with historical data.
    df = pd.DataFrame()
    env = make_env(df, {"features": ["close"], "lookback": 10, "fee": 0.001, "slippage": 0.001})

    for _ in range(epochs):
        env.reset()
        done = False
        while not done:
            # Random policy for placeholder purposes
            action = env.action_space.sample()
            _, _, done, _ = env.step(action)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--epochs", type=int, default=1)
    args = parser.parse_args()
    train(args.symbol, args.epochs)


if __name__ == "__main__":
    main()

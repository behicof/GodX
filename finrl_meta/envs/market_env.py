import numpy as np
import pandas as pd
import gym
from gym import spaces


class MarketEnv(gym.Env):
    """A minimal market environment following the Gym API.

    Parameters
    ----------
    df : pandas.DataFrame
        Time-indexed market data.
    cfg : dict
        Environment configuration with keys:
            - features: list of column names used as observations
            - lookback: number of timesteps in each observation window
            - fee: trading fee proportion per transaction
            - slippage: slippage proportion per transaction
    """

    metadata = {"render.modes": []}

    def __init__(self, df: pd.DataFrame, cfg: dict):
        super().__init__()
        self.df = df.reset_index(drop=True)
        self.features = cfg.get("features", ["close"])
        self.lookback = int(cfg.get("lookback", 1))
        self.fee = float(cfg.get("fee", 0.0))
        self.slippage = float(cfg.get("slippage", 0.0))

        obs_shape = (self.lookback * len(self.features),)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=obs_shape, dtype=np.float32
        )
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

        self.current_step = self.lookback
        self.position = 0.0
        self.pnl_history: list[float] = []

    # ------------------------------------------------------------------
    def reset(self):  # type: ignore[override]
        self.current_step = self.lookback
        self.position = 0.0
        self.pnl_history.clear()
        return self._get_observation()

    # ------------------------------------------------------------------
    def step(self, action):  # type: ignore[override]
        action = float(np.clip(action, -1.0, 1.0))
        prev_price = self.df["close"].iloc[self.current_step - 1]
        price = self.df["close"].iloc[self.current_step]

        prev_pos = self.position
        self.position = action
        trade = self.position - prev_pos

        fee_cost = abs(trade) * self.fee * price
        slip_cost = abs(trade) * self.slippage * price

        pnl = (price - prev_price) * prev_pos - fee_cost - slip_cost
        self.pnl_history.append(pnl)
        risk = np.std(self.pnl_history[-self.lookback :]) if len(self.pnl_history) > 1 else 0.0
        reward = pnl / (risk + 1e-8)

        self.current_step += 1
        done = self.current_step >= len(self.df)
        obs = self._get_observation() if not done else np.zeros(self.observation_space.shape, dtype=np.float32)
        info = {"pnl": pnl, "position": self.position}
        return obs, reward, done, info

    # ------------------------------------------------------------------
    def _get_observation(self) -> np.ndarray:
        window = self.df[self.features].iloc[
            self.current_step - self.lookback : self.current_step
        ]
        return window.values.flatten().astype(np.float32)


# ----------------------------------------------------------------------
def make_env(df: pd.DataFrame, cfg: dict) -> MarketEnv:
    """Factory function returning a MarketEnv instance."""
    return MarketEnv(df, cfg)

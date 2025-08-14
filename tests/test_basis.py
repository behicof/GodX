import pandas as pd

from research import BTConfig, simulate_basis


def test_simulate_basis_single_trade():
    df = pd.DataFrame(
        {
            "spot": [100, 101, 102, 103, 102, 101],
            "future": [105, 104, 103, 102, 103, 105],
        }
    )
    cfg = BTConfig(long_entry=0.02, short_entry=0.02)
    result = simulate_basis(df, cfg)
    assert result["trades"] == 1
    assert abs(result["pnl"] - 6) < 1e-9
    assert result["max_drawdown"] == 0.0

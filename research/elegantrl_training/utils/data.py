from __future__ import annotations

"""Utility functions for loading training data slices.

This module provides a helper for loading the ``train``, ``valid`` and
``forward`` data splits used by the ElegantRL training pipeline.
"""

from pathlib import Path
from typing import Dict

import pandas as pd


def load_data(env_cfg: dict) -> Dict[str, pd.DataFrame]:
    """Load train, validation and forward data for a given symbol.

    Parameters
    ----------
    env_cfg : dict
        Environment configuration containing at minimum ``symbol`` and
        optionally ``data_dir`` specifying the directory where data is stored.

    Returns
    -------
    dict[str, pandas.DataFrame]
        Mapping of slice name (``train``, ``valid``, ``forward``) to the loaded
        DataFrame.

    Raises
    ------
    FileNotFoundError
        If any of the expected parquet files are missing.
    """
    base_path = Path(env_cfg.get("data_dir", "data/parquet")) / env_cfg["symbol"]

    expected_slices = ["train", "valid", "forward"]
    missing = [s for s in expected_slices if not (base_path / f"{s}.parquet").is_file()]
    if missing:
        missing_str = ", ".join(sorted(missing))
        raise FileNotFoundError(
            f"Missing data files for slices: {missing_str} in {base_path}"
        )

    return {
        s: pd.read_parquet(base_path / f"{s}.parquet") for s in expected_slices
    }

from __future__ import annotations

from pathlib import Path
import pandas as pd


def extract_raw_data(input_path: str | Path) -> pd.DataFrame:
    """Read raw Superstore CSV exactly like the notebook logic."""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file raw data: {path}")
    return pd.read_csv(path)

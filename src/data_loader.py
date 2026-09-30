"""Read the project CSV data."""

from pathlib import Path

import pandas as pd

from src.config import RAW_DATA_PATH


def load_data(path: str | Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load a CSV file as a DataFrame."""
    return pd.read_csv(Path(path))

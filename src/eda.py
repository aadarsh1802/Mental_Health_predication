"""Small helpers for exploring the survey data."""

import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import TARGET_COLUMN


def summarize_data(data: pd.DataFrame) -> dict[str, object]:
    """Summarize the dataset's shape, columns, missing values, and duplicates."""
    return {
        "shape": data.shape,
        "dtypes": data.dtypes.astype(str),
        "missing_values": data.isna().sum(),
        "duplicate_rows": int(data.duplicated().sum()),
        "description": data.describe(include="all").transpose(),
    }


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicate rows."""
    return data.drop_duplicates().reset_index(drop=True)


def plot_target_distribution(
    data: pd.DataFrame, target: str = TARGET_COLUMN
) -> tuple[Figure, Axes]:
    """Plot a histogram for a numeric target column."""
    if target not in data.columns:
        raise KeyError(f"Target column {target!r} is not present in the data.")
    if not pd.api.types.is_numeric_dtype(data[target]):
        raise TypeError(f"Target column {target!r} must be numeric.")

    figure, axes = plt.subplots()
    axes.hist(data[target].dropna())
    axes.set_xlabel(target)
    axes.set_ylabel("Frequency")
    axes.set_title(f"Distribution of {target}")
    figure.tight_layout()
    return figure, axes


def plot_numeric_correlations(data: pd.DataFrame) -> tuple[Figure, Axes]:
    """Show correlations between numeric columns."""
    numeric_data = data.select_dtypes(include="number")
    if numeric_data.empty:
        raise ValueError("The dataset does not contain numeric columns.")

    figure, axes = plt.subplots(figsize=(10, 8))
    sns.heatmap(numeric_data.corr(), annot=True, ax=axes)
    axes.set_title("Numeric feature correlations")
    figure.tight_layout()
    return figure, axes

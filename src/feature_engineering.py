"""Prepare model inputs and assemble the training pipeline."""

import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

from src.config import RANDOM_STATE, TARGET_COLUMN
from src.preprocessing import build_preprocessor


def split_features_target(
    data: pd.DataFrame, target: str = TARGET_COLUMN
) -> tuple[pd.DataFrame, pd.Series]:
    """Separate the target and remove any index column saved from a CSV."""
    if target not in data.columns:
        raise KeyError(f"Target column {target!r} is not present in the data.")
    if data.columns.duplicated().any():
        raise ValueError("The dataset contains duplicate column names.")

    target_values = data[target]
    if target_values.isna().any():
        raise ValueError(f"Target column {target!r} contains missing values.")

    features = data.drop(columns=[target]).copy()
    index_columns = [
        column
        for column in features.columns
        if column.lower().startswith("unnamed:")
    ]
    features = features.drop(columns=index_columns)
    if features.empty or not len(features.columns):
        raise ValueError("No usable feature columns remain after cleanup.")
    return features, target_values.copy()


def build_model_pipeline(
    features: pd.DataFrame,
    estimator: RegressorMixin | None = None,
) -> Pipeline:
    """Put preprocessing and a regressor into one pipeline."""
    if estimator is None:
        estimator = RandomForestRegressor(
            n_estimators=300,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(features)),
            ("model", estimator),
        ]
    )

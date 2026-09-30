"""Load the saved model and predict mental health scores."""

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import MODEL_PATH
from src.utils import load_model as _load_model


def load_model(path: str | Path = MODEL_PATH) -> Any:
    """Load a trained model from disk."""
    return _load_model(path)


def _as_feature_frame(
    inputs: pd.DataFrame | Mapping[str, Any] | Sequence[Mapping[str, Any]],
) -> pd.DataFrame:
    if isinstance(inputs, pd.DataFrame):
        features = inputs.copy()
    elif isinstance(inputs, Mapping):
        features = pd.DataFrame([inputs])
    elif isinstance(inputs, Sequence) and not isinstance(inputs, (str, bytes)):
        features = pd.DataFrame(inputs)
    else:
        raise TypeError("Pass a DataFrame, a feature dictionary, or a list of dictionaries.")

    if features.empty:
        raise ValueError("At least one prediction row is required.")
    if features.columns.duplicated().any():
        raise ValueError("Prediction input contains duplicate column names.")
    return features


def predict_scores(
    model: Any,
    inputs: pd.DataFrame | Mapping[str, Any] | Sequence[Mapping[str, Any]],
) -> list[float]:
    """Predict scores for one record or a batch of records."""
    features = _as_feature_frame(inputs)
    expected_columns = getattr(model, "feature_names_in_", None)
    if expected_columns is not None:
        missing_columns = [
            column for column in expected_columns if column not in features.columns
        ]
        extra_columns = [
            column for column in features.columns if column not in expected_columns
        ]
        if missing_columns or extra_columns:
            details = []
            if missing_columns:
                details.append(f"missing columns: {missing_columns}")
            if extra_columns:
                details.append(f"unexpected columns: {extra_columns}")
            message = "; ".join(details)
            raise ValueError(f"Prediction feature schema mismatch ({message}).")
        features = features.loc[:, list(expected_columns)]

    return [float(value) for value in model.predict(features)]

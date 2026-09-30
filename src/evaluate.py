"""Evaluate and compare regression models."""

from collections.abc import Mapping

import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_model(
    model: RegressorMixin, features: pd.DataFrame, target: pd.Series
) -> dict[str, float]:
    """Return MAE, RMSE, and R-squared for a fitted model."""
    if len(features) != len(target):
        raise ValueError("Feature and target row counts must match.")
    if target.empty:
        raise ValueError("Cannot evaluate a model with no target values.")

    predictions = model.predict(features)
    return {
        "MAE": float(mean_absolute_error(target, predictions)),
        "RMSE": float(mean_squared_error(target, predictions) ** 0.5),
        "R2": float(r2_score(target, predictions)),
    }


def compare_models(
    models: Mapping[str, RegressorMixin],
    features: pd.DataFrame,
    target: pd.Series,
) -> pd.DataFrame:
    """Evaluate fitted models, best RMSE first."""
    rows = [
        {"Model": name, **evaluate_model(model, features, target)}
        for name, model in models.items()
    ]
    if not rows:
        raise ValueError("At least one fitted model is required.")
    return pd.DataFrame(rows).sort_values("RMSE", ascending=True).reset_index(
        drop=True
    )

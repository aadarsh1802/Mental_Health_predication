"""Train and save the mental health score model."""

from collections.abc import Callable
from pathlib import Path

import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.ensemble import (
    GradientBoostingRegressor,
    HistGradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.config import MODEL_PATH, RANDOM_STATE, TEST_SIZE
from src.data_loader import load_data
from src.eda import clean_data
from src.evaluate import evaluate_model
from src.feature_engineering import build_model_pipeline, split_features_target
from src.utils import get_logger, save_model

logger = get_logger(__name__)


def get_candidate_models() -> dict[str, Callable[[], RegressorMixin]]:
    """Return the regressors explored in the notebook."""
    return {
        "Linear Regression": LinearRegression,
        "Ridge Regression": lambda: Ridge(alpha=1.0),
        "Random Forest": lambda: RandomForestRegressor(
            n_estimators=300,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "Gradient Boosting": lambda: GradientBoostingRegressor(
            random_state=RANDOM_STATE
        ),
        "Hist Gradient Boosting": lambda: HistGradientBoostingRegressor(
            random_state=RANDOM_STATE
        ),
    }


def train_model(
    features: pd.DataFrame,
    target: pd.Series,
    estimator: RegressorMixin | None = None,
) -> Pipeline:
    """Fit a preprocessing and regression pipeline."""
    if len(features) != len(target):
        raise ValueError("Feature and target row counts must match.")
    if features.empty:
        raise ValueError("Cannot train a model with no rows.")

    pipeline = build_model_pipeline(features, estimator)
    return pipeline.fit(features, target)


def train_and_save_model(
    data: pd.DataFrame,
    model_path: str | Path = MODEL_PATH,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
) -> tuple[Pipeline, dict[str, float]]:
    """Train a random forest, check it on a holdout set, and save the pipeline."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")

    features, target = split_features_target(data)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
    )
    model = train_model(x_train, y_train)
    metrics = evaluate_model(model, x_test, y_test)
    saved_path = save_model(model, model_path)
    logger.info("Saved model to %s; evaluation metrics: %s", saved_path, metrics)
    return model, metrics


def main() -> None:
    """Train a model using the raw survey CSV."""
    train_and_save_model(clean_data(load_data()))


if __name__ == "__main__":
    main()

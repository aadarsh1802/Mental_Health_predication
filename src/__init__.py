"""Mental health score prediction package."""

from src.config import TARGET_COLUMN
from src.evaluate import evaluate_model
from src.feature_engineering import build_model_pipeline, split_features_target
from src.predict import predict_scores
from src.preprocessing import build_preprocessor
from src.train import train_model

__all__ = [
    "TARGET_COLUMN",
    "build_model_pipeline",
    "build_preprocessor",
    "evaluate_model",
    "predict_scores",
    "split_features_target",
    "train_model",
]
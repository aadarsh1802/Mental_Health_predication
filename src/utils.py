"""Logging and model file helpers."""

import logging
from pathlib import Path
from typing import Any

import joblib


def get_logger(name: str = "mental_health_score_predictor") -> logging.Logger:
    """Set up a logger for the project."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        )
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def save_model(model: Any, path: str | Path) -> Path:
    """Save a fitted model and return the file path."""
    model_path = Path(path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    return model_path


def load_model(path: str | Path) -> Any:
    """Load a model saved with joblib."""
    return joblib.load(Path(path))

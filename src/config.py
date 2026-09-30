"""Project paths and training defaults."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Student Social Media And Mental Health Impact.csv"
)
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_data.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "mental_health.pkl"
REPORTS_PATH = PROJECT_ROOT / "reports"

TARGET_COLUMN = "Mental_Health_Score"
RANDOM_STATE = 42
TEST_SIZE = 0.2

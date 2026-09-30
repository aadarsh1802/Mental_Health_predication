"""Build the preprocessing steps used by the model."""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def get_feature_columns(
    features: pd.DataFrame,
) -> tuple[list[str], list[str]]:
    """Split feature names into numeric and categorical columns."""
    numeric_columns = features.select_dtypes(include="number").columns.tolist()
    categorical_columns = [
        column for column in features.columns if column not in numeric_columns
    ]
    return numeric_columns, categorical_columns


def build_preprocessor(features: pd.DataFrame) -> ColumnTransformer:
    """Impute missing values, scale numbers, and encode categories."""
    if features.empty or features.shape[1] == 0:
        raise ValueError("At least one feature and one row are required.")

    numeric_columns, categorical_columns = get_feature_columns(features)
    transformers = []

    if numeric_columns:
        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )
        transformers.append(("num", numeric_pipeline, numeric_columns))

    if categorical_columns:
        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                (
                    "encoder",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                ),
            ]
        )
        transformers.append(("cat", categorical_pipeline, categorical_columns))

    return ColumnTransformer(transformers=transformers)

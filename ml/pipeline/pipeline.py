"""
Scikit-learn Pipeline construction and feature transformation assembly for PropValueAI.

Provides reusable factory functions to build the complete, leakage-free pipeline
connecting raw inputs to feature transformation, median/onehot imputation, and regression.
"""

from typing import Any
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml.common.transformers import PropertyFeatureTransformer


def create_preprocessor(scale_numeric: bool = False) -> ColumnTransformer:
    """
    Creates a ColumnTransformer for numeric and categorical features.

    - Numeric columns ('total_sqft', 'bhk', 'bath', 'balcony'):
      Median imputed; optionally scaled.
    - Categorical columns ('area_type'):
      Most frequent imputed; OneHotEncoded with handle_unknown='ignore'.
    """
    numeric_cols = ["total_sqft", "bhk", "bath", "balcony"]
    categorical_cols = ["area_type"]

    num_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        num_steps.append(("scaler", StandardScaler()))
    numeric_transformer = Pipeline(steps=num_steps)

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ],
        remainder="drop"
    )


def build_pipeline(regressor: Any, scale_numeric: bool = False) -> Pipeline:
    """
    Builds a complete end-to-end Pipeline from raw inputs to prediction.

    Pipeline stages:
    1. feature_transformer: PropertyFeatureTransformer (cleans sqft, bhk, area)
    2. preprocessor: ColumnTransformer (median imputation, onehot encoding)
    3. regressor: Fitted estimator (e.g. RandomForestRegressor)
    """
    return Pipeline(steps=[
        ("feature_transformer", PropertyFeatureTransformer()),
        ("preprocessor", create_preprocessor(scale_numeric=scale_numeric)),
        ("regressor", regressor),
    ])

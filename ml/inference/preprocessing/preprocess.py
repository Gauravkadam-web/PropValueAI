"""
Preprocessing and input preparation for the PropValueAI ML Inference Service.

Prepares validated feature dictionaries into pandas DataFrames ready for evaluation
by the fitted scikit-learn pipeline.
"""

from typing import Any, Dict, List
import pandas as pd


def prepare_feature_dataframe(feature_dicts: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Converts a list of property feature dictionaries into a pandas DataFrame
    matching the column schema expected by the fitted pipeline:
    ['total_sqft', 'size', 'bath', 'balcony', 'area_type'].

    Args:
        feature_dicts: List of dictionaries with property input features.

    Returns:
        pd.DataFrame formatted for pipeline.predict().
    """
    if not feature_dicts:
        return pd.DataFrame(columns=["total_sqft", "size", "bath", "balcony", "area_type"])

    df = pd.DataFrame(feature_dicts)

    # Ensure all required pipeline columns are present in DataFrame
    required_cols = ["total_sqft", "size", "bath", "balcony", "area_type"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    return df[required_cols]

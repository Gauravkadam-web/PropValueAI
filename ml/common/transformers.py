"""
Custom scikit-learn Transformers for PropValueAI.

Provides leakage-free, reproducible feature extraction and cleaning for property
area, bedroom count, and categorical attributes.
"""

import re
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from ml.common.constants import SQFT_UNIT_CONVERSIONS


def parse_sqft_value(val) -> float:
    """Parses a total_sqft value into square feet as float. Returns np.nan on failure."""
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val) if val > 0 else np.nan

    val_str = str(val).strip()
    # Try pure float conversion
    try:
        f = float(val_str)
        return f if f > 0 else np.nan
    except ValueError:
        pass

    # Check for range pattern (e.g. "2100 - 2850")
    if "-" in val_str:
        tokens = val_str.split("-")
        if len(tokens) == 2:
            try:
                low = float(tokens[0].strip())
                high = float(tokens[1].strip())
                if low > 0 and high > 0:
                    return (low + high) / 2.0
            except ValueError:
                return np.nan

    # Check for recognized units
    val_lower = val_str.lower()
    for unit, factor in SQFT_UNIT_CONVERSIONS.items():
        if unit in val_lower:
            # Extract the numeric component
            match = re.search(r"(\d+(?:\.\d+)?)", val_lower)
            if match:
                try:
                    num = float(match.group(1))
                    if num > 0:
                        return num * factor
                except ValueError:
                    return np.nan

    return np.nan


def parse_bhk_value(val) -> float:
    """Extracts integer bedroom count from size string or numeric input. Returns np.nan on failure."""
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val) if val > 0 else np.nan

    match = re.search(r"(\d+)", str(val))
    if match:
        bhk = int(match.group(1))
        return float(bhk) if bhk > 0 else np.nan
    return np.nan


class PropertyFeatureTransformer(BaseEstimator, TransformerMixin):
    """
    Scikit-learn compatible transformer that extracts and standardizes:
      - total_sqft (cleaned float in sqft)
      - bhk (parsed integer bedroom count)
      - bath (numeric float)
      - balcony (numeric float)
      - area_type (standardized string)
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        # Stateless transformer
        return self

    def transform(self, X):
        # Convert dict or list of dicts to DataFrame
        if isinstance(X, dict):
            df = pd.DataFrame([X])
        elif isinstance(X, list):
            df = pd.DataFrame(X)
        elif isinstance(X, pd.DataFrame):
            df = X.copy()
        else:
            raise TypeError(f"Unsupported input type for PropertyFeatureTransformer: {type(X)}")

        # Normalize column names: strip whitespace
        df.columns = [str(c).strip() for c in df.columns]

        # 1. total_sqft
        if "total_sqft" in df.columns:
            clean_sqft = df["total_sqft"].apply(parse_sqft_value)
        else:
            clean_sqft = pd.Series(np.nan, index=df.index)

        # 2. bhk (from 'bhk' or 'size')
        if "bhk" in df.columns:
            clean_bhk = df["bhk"].apply(parse_bhk_value)
        elif "size" in df.columns:
            clean_bhk = df["size"].apply(parse_bhk_value)
        else:
            clean_bhk = pd.Series(np.nan, index=df.index)

        # 3. bath
        if "bath" in df.columns:
            clean_bath = pd.to_numeric(df["bath"], errors="coerce")
        else:
            clean_bath = pd.Series(np.nan, index=df.index)

        # 4. balcony
        if "balcony" in df.columns:
            clean_balcony = pd.to_numeric(df["balcony"], errors="coerce")
        else:
            clean_balcony = pd.Series(np.nan, index=df.index)

        # 5. area_type
        if "area_type" in df.columns:
            clean_area_type = df["area_type"].astype(str).str.strip().replace("nan", np.nan)
        else:
            clean_area_type = pd.Series(np.nan, index=df.index)

        return pd.DataFrame({
            "total_sqft": clean_sqft,
            "bhk": clean_bhk,
            "bath": clean_bath,
            "balcony": clean_balcony,
            "area_type": clean_area_type,
        }, index=df.index)

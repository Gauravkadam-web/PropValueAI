"""
Custom scikit-learn Transformers for PropValueAI.

Provides leakage-free, reproducible feature extraction and cleaning for property
area, bedroom count, and categorical attributes.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from ml.common.constants import SQFT_UNIT_CONVERSIONS
from ml.common.utils import parse_sqft_value, parse_bhk_value


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

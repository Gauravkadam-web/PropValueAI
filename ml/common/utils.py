"""
Shared parsing and numerical utility functions for PropValueAI.

Provides leakage-free parsing and unit conversion for property area (total_sqft)
and bedroom count (size / bhk).
"""

import re
from typing import Any, Union
import numpy as np
import pandas as pd

from ml.common.constants import SQFT_UNIT_CONVERSIONS


def parse_sqft_value(val: Any) -> float:
    """
    Parses a total_sqft value into square feet as float.
    Handles numeric values, range strings ('2100 - 2850'), and recognized units ('1000Sq. Meter', '1Acres').
    Returns np.nan on failure or non-positive value.
    """
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val) if val > 0 else np.nan

    val_str = str(val).strip()
    if not val_str:
        return np.nan

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
            match = re.search(r"(\d+(?:\.\d+)?)", val_lower)
            if match:
                try:
                    num = float(match.group(1))
                    if num > 0:
                        return num * factor
                except ValueError:
                    return np.nan

    return np.nan


def parse_bhk_value(val: Any) -> float:
    """
    Parses a bedroom count specification into a numerical float.
    Handles numeric values and strings (e.g. '2 BHK', '3 Bedroom', '1 RK').
    Returns np.nan on failure or non-positive value.
    """
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val) if val > 0 else np.nan

    val_str = str(val).strip()
    if not val_str:
        return np.nan

    # Try pure float conversion
    try:
        f = float(val_str)
        return f if f > 0 else np.nan
    except ValueError:
        pass

    match = re.search(r"(\d+(?:\.\d+)?)", val_str)
    if match:
        try:
            num = float(match.group(1))
            return num if num > 0 else np.nan
        except ValueError:
            return np.nan

    return np.nan

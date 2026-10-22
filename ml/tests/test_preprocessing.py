"""
Unit tests for data preprocessing and custom transformers in PropValueAI.
"""

import math
import numpy as np
import pandas as pd
import pytest

from ml.common.transformers import (
    parse_sqft_value,
    parse_bhk_value,
    PropertyFeatureTransformer,
)
from ml.pipeline.pipeline import create_preprocessor, build_pipeline
from sklearn.dummy import DummyRegressor


def test_area_numeric_parsing():
    """Verify standard numeric values parse correctly."""
    assert parse_sqft_value(1056) == 1056.0
    assert parse_sqft_value("1200") == 1200.0
    assert parse_sqft_value("1440.5") == 1440.5


def test_area_range_conversion():
    """Verify area range intervals are correctly converted to their midpoint."""
    assert parse_sqft_value("2100 - 2850") == 2475.0
    assert parse_sqft_value("1000 - 1200") == 1100.0
    assert parse_sqft_value("500 - 600") == 550.0


def test_recognized_unit_conversions():
    """Verify alternative area units are converted to square feet using exact factors."""
    # Sq. Meter: factor 10.7639
    sq_meter_val = parse_sqft_value("100Sq. Meter")
    assert math.isclose(sq_meter_val, 1076.39, rel_tol=1e-3)

    # Sq. Yards: factor 9.0
    sq_yard_val = parse_sqft_value("1000Sq. Yards")
    assert math.isclose(sq_yard_val, 9000.0, rel_tol=1e-3)

    # Acres: factor 43560.0
    acres_val = parse_sqft_value("1Acres")
    assert math.isclose(acres_val, 43560.0, rel_tol=1e-3)

    # Guntha: factor 1089.0
    guntha_val = parse_sqft_value("2Guntha")
    assert math.isclose(guntha_val, 2178.0, rel_tol=1e-3)

    # Cents: factor 435.6
    cents_val = parse_sqft_value("10Cents")
    assert math.isclose(cents_val, 4356.0, rel_tol=1e-3)


def test_invalid_and_missing_area_values():
    """Verify invalid, non-positive, or unparseable area values return np.nan."""
    assert np.isnan(parse_sqft_value(np.nan))
    assert np.isnan(parse_sqft_value(None))
    assert np.isnan(parse_sqft_value(""))
    assert np.isnan(parse_sqft_value("   "))
    assert np.isnan(parse_sqft_value("invalid_text"))
    assert np.isnan(parse_sqft_value("abc - def"))
    assert np.isnan(parse_sqft_value(-500))
    assert np.isnan(parse_sqft_value("-100 - -200"))


def test_bedroom_parsing():
    """Verify bedroom parsing extracts integer BHK across diverse naming conventions."""
    assert parse_bhk_value("2 BHK") == 2.0
    assert parse_bhk_value("4 Bedroom") == 4.0
    assert parse_bhk_value("1 RK") == 1.0
    assert parse_bhk_value("10 BHK") == 10.0
    assert parse_bhk_value(3) == 3.0
    assert parse_bhk_value(3.0) == 3.0
    assert np.isnan(parse_bhk_value(np.nan))
    assert np.isnan(parse_bhk_value(""))
    assert np.isnan(parse_bhk_value("Studio"))


def test_property_feature_transformer_dataframe():
    """Verify PropertyFeatureTransformer standardizes DataFrame features."""
    transformer = PropertyFeatureTransformer()
    sample_df = pd.DataFrame({
        "total_sqft": ["1200", "2100 - 2850", "1000Sq. Yards", "invalid"],
        "size": ["2 BHK", "4 Bedroom", "1 RK", np.nan],
        "bath": [2.0, 4.0, np.nan, 1.0],
        "balcony": [1.0, np.nan, 2.0, 0.0],
        "area_type": ["Super built-up  Area", "Plot  Area", "Built-up  Area", np.nan],
    })

    transformed = transformer.fit_transform(sample_df)

    assert isinstance(transformed, pd.DataFrame)
    assert list(transformed.columns) == ["total_sqft", "bhk", "bath", "balcony", "area_type"]
    assert transformed["total_sqft"].iloc[0] == 1200.0
    assert transformed["total_sqft"].iloc[1] == 2475.0
    assert transformed["total_sqft"].iloc[2] == 9000.0
    assert np.isnan(transformed["total_sqft"].iloc[3])
    assert transformed["bhk"].iloc[0] == 2.0
    assert transformed["bhk"].iloc[1] == 4.0
    assert transformed["bhk"].iloc[2] == 1.0
    assert np.isnan(transformed["bhk"].iloc[3])


def test_unseen_categorical_values_in_pipeline():
    """Verify pipeline handles previously unseen categorical area types safely without erroring."""
    X_train = pd.DataFrame({
        "total_sqft": ["1000", "1500"],
        "size": ["2 BHK", "3 BHK"],
        "bath": [2.0, 3.0],
        "balcony": [1.0, 2.0],
        "area_type": ["Super built-up  Area", "Built-up  Area"],
    })
    y_train = np.array([50.0, 75.0])

    pipeline = build_pipeline(DummyRegressor(strategy="mean"))
    pipeline.fit(X_train, y_train)

    # Test with unseen category 'Ultra Luxury Penthouse' and missing bath
    X_unseen = pd.DataFrame({
        "total_sqft": ["2000"],
        "size": ["4 BHK"],
        "bath": [np.nan],
        "balcony": [1.0],
        "area_type": ["Ultra Luxury Penthouse"],
    })

    pred = pipeline.predict(X_unseen)
    assert len(pred) == 1
    assert np.isfinite(pred[0])
    assert math.isclose(pred[0], 62.5, rel_tol=1e-3)

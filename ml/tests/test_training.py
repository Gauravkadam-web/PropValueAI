"""
Unit tests for pipeline construction, reproducibility, and training workflows.
"""

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from ml.common.constants import RANDOM_SEED, TEST_SPLIT_RATIO
from ml.pipeline.pipeline import build_pipeline
from ml.training.scripts.train import filter_training_outliers


@pytest.fixture
def sample_property_data():
    """Provides a small synthetic test fixture for unit testing."""
    return pd.DataFrame({
        "total_sqft": ["1000", "1200", "1500", "1800", "2200", "2500", "3000", "3500"],
        "size": ["2 BHK", "2 BHK", "3 BHK", "3 BHK", "3 BHK", "4 BHK", "4 BHK", "5 BHK"],
        "bath": [2.0, 2.0, 2.0, 3.0, 3.0, 4.0, 4.0, 5.0],
        "balcony": [1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0],
        "area_type": [
            "Super built-up  Area",
            "Built-up  Area",
            "Super built-up  Area",
            "Built-up  Area",
            "Plot  Area",
            "Super built-up  Area",
            "Plot  Area",
            "Plot  Area"
        ],
        "price": [45.0, 52.0, 68.0, 80.0, 110.0, 135.0, 180.0, 220.0]
    })


def test_pipeline_output_shape_and_finite_predictions(sample_property_data):
    """Verify end-to-end pipeline produces expected 1D numeric array of finite values."""
    X = sample_property_data[["total_sqft", "size", "bath", "balcony", "area_type"]]
    y = sample_property_data["price"]

    pipeline = build_pipeline(LinearRegression(), scale_numeric=True)
    pipeline.fit(X, y)

    preds = pipeline.predict(X)
    assert isinstance(preds, np.ndarray)
    assert preds.shape == (len(X),)
    assert np.all(np.isfinite(preds))


def test_reproducible_splitting():
    """Verify train_test_split produces identical subsets given fixed seed."""
    df = pd.DataFrame({
        "id": range(100),
        "val": range(100)
    })

    train1, test1 = train_test_split(df, test_size=TEST_SPLIT_RATIO, random_state=RANDOM_SEED)
    train2, test2 = train_test_split(df, test_size=TEST_SPLIT_RATIO, random_state=RANDOM_SEED)

    pd.testing.assert_frame_equal(train1, train2)
    pd.testing.assert_frame_equal(test1, test2)


def test_training_outlier_filtering_rules():
    """Verify outlier filtering logic removes implausible sqft/bhk and excessive bathrooms."""
    anomalous_df = pd.DataFrame({
        "total_sqft": ["200", "1200", "2000", "1000"],
        "size": ["4 BHK", "2 BHK", "2 BHK", "2 BHK"],  # 200/4 = 50 sqft/bhk (anomaly)
        "bath": [2.0, 2.0, 6.0, 2.0],  # 6 baths with 2 BHK (anomaly)
        "price": [50.0, 60.0, 90.0, 0.01],  # 0.01 Lakhs for 1000 sqft = 1 INR/sqft (anomaly)
    })

    filtered = filter_training_outliers(anomalous_df)
    # Only row index 1 (1200 sqft, 2 BHK, 2 bath, 60 Lakhs) is valid
    assert len(filtered) == 1
    assert filtered.iloc[0]["total_sqft"] == "1200"


def test_pipeline_tree_regressor(sample_property_data):
    """Verify tree-based pipeline fits and predicts correctly without numeric scaling."""
    X = sample_property_data[["total_sqft", "size", "bath", "balcony", "area_type"]]
    y = sample_property_data["price"]

    rf_pipeline = build_pipeline(
        RandomForestRegressor(n_estimators=10, random_state=RANDOM_SEED),
        scale_numeric=False
    )
    rf_pipeline.fit(X, y)

    query = pd.DataFrame([{
        "total_sqft": "1600",
        "size": "3 BHK",
        "bath": 2.0,
        "balcony": 2.0,
        "area_type": "Super built-up  Area"
    }])

    pred = rf_pipeline.predict(query)
    assert len(pred) == 1
    assert pred[0] > 0
    assert np.isfinite(pred[0])

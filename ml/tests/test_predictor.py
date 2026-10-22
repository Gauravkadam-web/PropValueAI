"""
Unit tests for model artifact loading, prediction consistency, and metadata verification.
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def artifacts_paths():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "inference", "artifacts"))
    model_path = os.path.join(base_dir, "model.joblib")
    meta_path = os.path.join(base_dir, "metadata.json")
    return model_path, meta_path


def test_artifacts_exist(artifacts_paths):
    """Verify saved model.joblib and metadata.json exist."""
    model_path, meta_path = artifacts_paths
    assert os.path.isfile(model_path), f"Artifact missing: {model_path}"
    assert os.path.isfile(meta_path), f"Metadata missing: {meta_path}"


def test_metadata_schema(artifacts_paths):
    """Verify metadata.json contains all required architectural and evaluation fields."""
    _, meta_path = artifacts_paths
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    required_keys = [
        "project",
        "phase",
        "model_name",
        "model_class",
        "target_variable",
        "target_unit",
        "feature_schema",
        "preprocessing",
        "training_data",
        "evaluation_metrics",
        "candidate_comparison",
        "environment",
        "limitations",
    ]
    for key in required_keys:
        assert key in meta, f"Missing key in metadata: {key}"

    assert meta["target_variable"] == "price"
    assert meta["target_unit"] == "Lakhs INR"
    assert meta["training_data"]["total_raw_rows"] == 13320
    assert meta["evaluation_metrics"]["test_r2"] > 0.50
    assert "Educational demonstration only" in meta["limitations"]


def test_artifact_prediction_consistency(artifacts_paths):
    """Verify loaded pipeline predicts successfully on single record and batch input."""
    model_path, _ = artifacts_paths
    pipeline = joblib.load(model_path)

    # 1. Single sample input (2 BHK, 1200 sqft, 2 bath, 1 balcony, Super built-up Area)
    single_record = pd.DataFrame([{
        "total_sqft": "1200",
        "size": "2 BHK",
        "bath": 2.0,
        "balcony": 1.0,
        "area_type": "Super built-up  Area"
    }])
    pred_single = pipeline.predict(single_record)
    assert len(pred_single) == 1
    assert pred_single[0] > 0
    assert np.isfinite(pred_single[0])

    # 2. Batch input
    batch_records = pd.DataFrame([
        {
            "total_sqft": "1056",
            "size": "2 BHK",
            "bath": 2.0,
            "balcony": 1.0,
            "area_type": "Super built-up  Area"
        },
        {
            "total_sqft": "2600",
            "size": "4 Bedroom",
            "bath": 5.0,
            "balcony": 3.0,
            "area_type": "Plot  Area"
        },
        {
            "total_sqft": "2100 - 2850",  # Range string
            "size": "3 BHK",
            "bath": 3.0,
            "balcony": 2.0,
            "area_type": "Built-up  Area"
        }
    ])
    pred_batch = pipeline.predict(batch_records)
    assert len(pred_batch) == 3
    assert np.all(pred_batch > 0)
    assert np.all(np.isfinite(pred_batch))

    # Larger property should predict higher price than smaller one
    assert pred_batch[1] > pred_batch[0]

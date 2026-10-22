"""
Unit and integration tests for newly refactored ML architectural modules.

Verifies:
- ml.pipeline.pipeline (pipeline and preprocessor construction)
- ml.common.utils (shared parsing utilities)
- ml.inference.model.loader (isolated artifact loading and verification)
- ml.inference.preprocessing.preprocess (feature DataFrame preparation)
- ml.inference.services.prediction_service (prediction orchestration and disclaimer)
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from sklearn.dummy import DummyRegressor

from ml.common.utils import parse_sqft_value, parse_bhk_value
from ml.pipeline.pipeline import create_preprocessor, build_pipeline
from ml.inference.config.settings import settings
from ml.inference.model.loader import (
    load_model_artifact,
    load_metadata,
    verify_pipeline_integrity,
    load_and_verify_pipeline,
)
from ml.inference.preprocessing.preprocess import prepare_feature_dataframe
from ml.inference.services.prediction_service import PredictionService


def test_common_utils_parsing():
    """Verify shared parsing utilities in ml.common.utils."""
    assert parse_sqft_value(1200) == 1200.0
    assert parse_sqft_value("2100 - 2900") == 2500.0
    assert parse_sqft_value("1000Sq. Meter") > 10000.0
    assert np.isnan(parse_sqft_value(-500))
    assert np.isnan(parse_sqft_value("invalid"))

    assert parse_bhk_value(2) == 2.0
    assert parse_bhk_value("3 BHK") == 3.0
    assert parse_bhk_value("4 Bedroom") == 4.0
    assert np.isnan(parse_bhk_value(-1))


def test_pipeline_factory():
    """Verify create_preprocessor and build_pipeline in ml.pipeline.pipeline."""
    preprocessor = create_preprocessor(scale_numeric=False)
    assert preprocessor is not None
    assert "num" in [t[0] for t in preprocessor.transformers]
    assert "cat" in [t[0] for t in preprocessor.transformers]

    dummy = DummyRegressor(strategy="mean")
    pipe = build_pipeline(dummy, scale_numeric=True)
    assert pipe is not None
    assert "feature_transformer" in pipe.named_steps
    assert "preprocessor" in pipe.named_steps
    assert "regressor" in pipe.named_steps


def test_model_loader_isolated():
    """Verify isolated artifact and metadata loading from ml.inference.model.loader."""
    pipeline, meta = load_and_verify_pipeline(settings.model_path, settings.metadata_path)
    assert pipeline is not None
    assert hasattr(pipeline, "predict")
    assert isinstance(meta, dict)
    assert meta.get("target_unit") == "Lakhs INR"


def test_preprocessing_feature_dataframe():
    """Verify prepare_feature_dataframe formats all required columns."""
    sample = [{"total_sqft": 1200, "size": "2 BHK", "bath": 2.0}]
    df = prepare_feature_dataframe(sample)
    assert list(df.columns) == ["total_sqft", "size", "bath", "balcony", "area_type"]
    assert df.loc[0, "total_sqft"] == 1200
    assert df.loc[0, "balcony"] is None


def test_prediction_service_orchestration():
    """Verify PredictionService attaches disclaimer, model version, and generates UUIDs."""
    service = PredictionService()
    res = service.predict_single({
        "total_sqft": 1056.0,
        "size": "2 BHK",
        "bath": 2.0,
        "balcony": 1.0,
        "area_type": "Super built-up  Area",
    })
    assert "prediction_id" in res
    assert res["predicted_price"] > 0
    assert res["target_unit"] == "Lakhs INR"
    assert res["model_name"] == "Random Forest"
    assert "PropValueAI provides simulated estimates" in res["disclaimer"]

    info = service.get_model_info()
    assert info["model_name"] == "Random Forest"
    assert info["target_variable"] == "price"

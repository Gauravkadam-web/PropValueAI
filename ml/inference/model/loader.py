"""
Model artifact deserialization and metadata validation for PropValueAI ML Inference Service.

Responsible for safely loading the serialized scikit-learn pipeline, validating its
deserialized structure and fitted state, and loading architectural metadata.
"""

import json
import logging
import math
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import joblib
import pandas as pd

logger = logging.getLogger(__name__)


class ModelNotReadyError(Exception):
    """Raised when inference is requested before model is loaded or if load failed."""
    pass


class ArtifactLoadError(Exception):
    """Raised when an artifact file is missing, corrupt, or invalid."""
    pass


def load_model_artifact(model_path: Path) -> Any:
    """
    Loads and deserializes the scikit-learn pipeline artifact using joblib.

    Raises:
        ArtifactLoadError: If file is missing, cannot be deserialized, or lacks a predict method.
    """
    if not model_path.exists():
        raise ArtifactLoadError(f"Model artifact not found at path: {model_path}")

    try:
        loaded_artifact = joblib.load(model_path)
    except Exception as e:
        raise ArtifactLoadError(f"Failed to deserialize model artifact: {str(e)}") from e

    if not hasattr(loaded_artifact, "predict"):
        raise ArtifactLoadError("Loaded artifact does not possess a 'predict' method.")

    return loaded_artifact


def load_metadata(metadata_path: Path) -> Dict[str, Any]:
    """
    Loads and parses the architectural metadata.json file.
    Returns empty dictionary if metadata is missing or invalid, logging a warning.
    """
    if not metadata_path.exists():
        logger.warning(f"Metadata file not found at: {metadata_path}. Using default configuration.")
        return {}

    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            logger.info(f"Loaded metadata successfully from {metadata_path}")
            return meta
    except Exception as e:
        logger.warning(f"Could not parse metadata.json at {metadata_path}: {e}")
        return {}


def verify_pipeline_integrity(pipeline: Any) -> None:
    """
    Executes a sanity-check inference call on a synthetic record to guarantee
    the pipeline is fully fitted and produces valid, finite numerical output.

    Raises:
        ArtifactLoadError: If verification prediction fails or produces non-finite output.
    """
    try:
        dummy_input = pd.DataFrame([{
            "total_sqft": "1000",
            "size": "2 BHK",
            "bath": 2.0,
            "balcony": 1.0,
            "area_type": "Super built-up  Area"
        }])
        test_pred = pipeline.predict(dummy_input)
        if len(test_pred) != 1 or math.isnan(test_pred[0]) or math.isinf(test_pred[0]):
            raise ValueError("Verification prediction returned non-finite value.")
    except Exception as e:
        raise ArtifactLoadError(f"Pipeline verification prediction failed: {str(e)}") from e


def load_and_verify_pipeline(
    model_path: Path,
    metadata_path: Path,
) -> Tuple[Any, Dict[str, Any]]:
    """
    Loads model artifact, loads metadata, and runs integrity verification.

    Returns:
        Tuple of (fitted_pipeline, metadata_dict)
    """
    pipeline = load_model_artifact(model_path)
    metadata = load_metadata(metadata_path)
    verify_pipeline_integrity(pipeline)
    return pipeline, metadata

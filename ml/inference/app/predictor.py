"""
Model loading and inference manager for the PropValueAI ML Inference Service.

Loads the fitted scikit-learn pipeline once during application startup,
verifies pipeline integrity and metadata, and performs robust, finite predictions.
"""

import json
import logging
import math
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd
import joblib

from ml.inference.app.config import settings

logger = logging.getLogger(__name__)


class ModelNotReadyError(Exception):
    """Raised when an inference request is received before model is loaded or if load failed."""
    pass


class InferenceError(Exception):
    """Raised when an internal error occurs during pipeline prediction."""
    pass


class ModelPredictor:
    """Manages the lifecycle and inference execution of the fitted scikit-learn pipeline."""

    def __init__(self, model_path: Optional[Path] = None, metadata_path: Optional[Path] = None):
        self.model_path = model_path or settings.model_path
        self.metadata_path = metadata_path or settings.metadata_path
        self.pipeline: Any = None
        self.metadata: Dict[str, Any] = {}
        self.is_ready: bool = False
        self.load_error: Optional[str] = None
        self.model_name: str = "Random Forest"
        self.model_version: str = "1.0.0"
        self.target_unit: str = "Lakhs INR"

    def load_model(self) -> bool:
        """
        Loads the serialized pipeline artifact and associated metadata.
        Returns True if loading succeeded and model is verified fitted, False otherwise.
        """
        logger.info(f"Attempting to load model artifact from: {self.model_path}")

        # 1. Check if model artifact exists
        if not self.model_path.exists():
            self.is_ready = False
            self.load_error = f"Model artifact not found at path: {self.model_path}"
            logger.error(self.load_error)
            return False

        # 2. Attempt joblib load
        try:
            loaded_artifact = joblib.load(self.model_path)
        except Exception as e:
            self.is_ready = False
            self.load_error = f"Failed to deserialize model artifact: {str(e)}"
            logger.error(self.load_error, exc_info=True)
            return False

        # 3. Verify artifact structure
        if not hasattr(loaded_artifact, "predict"):
            self.is_ready = False
            self.load_error = "Loaded artifact does not possess a 'predict' method."
            logger.error(self.load_error)
            return False

        self.pipeline = loaded_artifact

        # 4. Load metadata if present
        if self.metadata_path.exists():
            try:
                with open(self.metadata_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                    self.model_name = self.metadata.get("model_name", self.model_name)
                    self.model_version = self.metadata.get("model_version", self.model_version)
                    self.target_unit = self.metadata.get("target_unit", self.target_unit)
                logger.info(f"Loaded metadata successfully. Model: {self.model_name} v{self.model_version}")
            except Exception as e:
                logger.warning(f"Could not parse metadata.json at {self.metadata_path}: {e}")
        else:
            logger.warning(f"Metadata file not found at: {self.metadata_path}. Using default configuration.")

        # 5. Sanity check prediction to verify pipeline is fitted
        try:
            dummy_input = pd.DataFrame([{
                "total_sqft": "1000",
                "size": "2 BHK",
                "bath": 2.0,
                "balcony": 1.0,
                "area_type": "Super built-up  Area"
            }])
            test_pred = self.pipeline.predict(dummy_input)
            if len(test_pred) != 1 or math.isnan(test_pred[0]) or math.isinf(test_pred[0]):
                raise ValueError("Verification prediction returned non-finite value.")
        except Exception as e:
            self.is_ready = False
            self.load_error = f"Pipeline verification prediction failed: {str(e)}"
            logger.error(self.load_error, exc_info=True)
            return False

        self.is_ready = True
        self.load_error = None
        logger.info(f"Model artifact successfully loaded and verified ready for inference.")
        return True

    def predict_single(self, feature_dict: Dict[str, Any]) -> float:
        """
        Executes inference for a single validated property dictionary.
        Returns predicted price in Lakhs INR rounded to 2 decimal places.
        """
        if not self.is_ready or self.pipeline is None:
            raise ModelNotReadyError(self.load_error or "Model is not initialized or ready for inference.")

        df = pd.DataFrame([feature_dict])
        try:
            preds = self.pipeline.predict(df)
            val = float(preds[0])
            if math.isnan(val) or math.isinf(val):
                raise InferenceError("Model generated a non-finite prediction.")
            # Non-negative policy: real-estate valuations cannot be negative
            clean_val = max(0.0, val)
            return round(clean_val, 2)
        except Exception as e:
            if isinstance(e, InferenceError):
                raise
            raise InferenceError(f"Prediction execution failed: {str(e)}") from e

    def predict_batch(self, feature_dicts: List[Dict[str, Any]]) -> List[float]:
        """
        Executes inference for a batch of validated property dictionaries.
        Preserves original input ordering and returns predicted prices in Lakhs INR.
        """
        if not self.is_ready or self.pipeline is None:
            raise ModelNotReadyError(self.load_error or "Model is not initialized or ready for inference.")

        if not feature_dicts:
            return []

        df = pd.DataFrame(feature_dicts)
        try:
            preds = self.pipeline.predict(df)
            results: List[float] = []
            for p in preds:
                val = float(p)
                if math.isnan(val) or math.isinf(val):
                    raise InferenceError("Model generated a non-finite prediction within batch.")
                results.append(round(max(0.0, val), 2))
            return results
        except Exception as e:
            if isinstance(e, InferenceError):
                raise
            raise InferenceError(f"Batch prediction execution failed: {str(e)}") from e


# Global predictor instance managed across application lifespan
predictor = ModelPredictor()

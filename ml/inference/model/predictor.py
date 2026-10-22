"""
Inference prediction engine for the PropValueAI ML Inference Service.

Coordinates model loading via loader.py and executes single and batch predictions
using the fitted scikit-learn pipeline with non-negative rounding guarantees.
"""

import logging
import math
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd

from ml.inference.config.settings import settings
from ml.inference.model.loader import (
    ArtifactLoadError,
    ModelNotReadyError,
    load_and_verify_pipeline,
)

logger = logging.getLogger(__name__)


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
        Loads the serialized pipeline artifact and associated metadata via loader.
        Returns True if loading succeeded and model is verified fitted, False otherwise.
        """
        logger.info(f"Attempting to load model artifact from: {self.model_path}")
        try:
            self.pipeline, self.metadata = load_and_verify_pipeline(
                self.model_path,
                self.metadata_path,
            )
            self.model_name = self.metadata.get("model_name", self.model_name)
            self.model_version = self.metadata.get("model_version", self.model_version)
            self.target_unit = self.metadata.get("target_unit", self.target_unit)
            self.is_ready = True
            self.load_error = None
            logger.info(
                f"Model artifact successfully loaded and verified ready for inference. "
                f"Model: {self.model_name} v{self.model_version}"
            )
            return True
        except ArtifactLoadError as e:
            self.is_ready = False
            self.load_error = str(e)
            logger.error(f"Model load failure: {self.load_error}")
            return False
        except Exception as e:
            self.is_ready = False
            self.load_error = f"Unexpected error loading model: {str(e)}"
            logger.error(self.load_error, exc_info=True)
            return False

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

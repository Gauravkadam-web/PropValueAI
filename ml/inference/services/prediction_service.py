"""
Prediction service orchestration for the PropValueAI ML Inference Service.

Encapsulates business logic, UUID generation, response assembling,
and educational disclaimer attachment for single and batch predictions.
"""

import uuid
from typing import Any, Dict, List, Optional

from ml.inference.config.settings import settings
from ml.inference.model.predictor import ModelPredictor, predictor


class PredictionService:
    """Orchestrates prediction requests and formats domain responses."""

    def __init__(self, model_predictor: Optional[ModelPredictor] = None):
        self.predictor = model_predictor or predictor

    def predict_single(self, feature_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates single property price prediction.

        Returns dictionary formatted for PropertyPredictResponse:
        - prediction_id: UUID string
        - predicted_price: float in Lakhs INR
        - target_unit: 'Lakhs INR'
        - model_name: string
        - model_version: string
        - disclaimer: educational disclaimer text
        """
        predicted_price = self.predictor.predict_single(feature_dict)
        return {
            "prediction_id": str(uuid.uuid4()),
            "predicted_price": predicted_price,
            "target_unit": self.predictor.target_unit,
            "model_name": self.predictor.model_name,
            "model_version": self.predictor.model_version,
            "disclaimer": settings.disclaimer,
        }

    def predict_batch(self, feature_dicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Orchestrates batch property price prediction for 1 to 100 properties.

        Returns dictionary formatted for PropertyBatchPredictResponse:
        - predictions: list of individual prediction responses
        - count: total count
        - model_name: string
        - model_version: string
        - disclaimer: educational disclaimer text
        """
        prices = self.predictor.predict_batch(feature_dicts)
        predictions = [
            {
                "prediction_id": str(uuid.uuid4()),
                "predicted_price": price,
                "target_unit": self.predictor.target_unit,
                "model_name": self.predictor.model_name,
                "model_version": self.predictor.model_version,
                "disclaimer": settings.disclaimer,
            }
            for price in prices
        ]
        return {
            "predictions": predictions,
            "count": len(predictions),
            "model_name": self.predictor.model_name,
            "model_version": self.predictor.model_version,
            "disclaimer": settings.disclaimer,
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Retrieves architectural metadata and limitations from the loaded model."""
        meta = self.predictor.metadata or {}
        return {
            "model_name": self.predictor.model_name,
            "model_version": self.predictor.model_version,
            "target_variable": meta.get("target_variable", "price"),
            "target_unit": self.predictor.target_unit,
            "feature_schema": meta.get("feature_schema", {
                "features": ["total_sqft", "size", "bath", "balcony", "area_type"],
            }),
            "evaluation_metrics": meta.get("evaluation_metrics", {}),
            "limitations": meta.get("limitations", settings.disclaimer),
        }

    def get_readiness(self) -> Dict[str, Any]:
        """Returns readiness status and model loading information."""
        if self.predictor.is_ready:
            return {
                "status": "ready",
                "model_loaded": True,
                "model_name": self.predictor.model_name,
                "model_version": self.predictor.model_version,
                "target_unit": self.predictor.target_unit,
                "details": "Model artifact loaded and verified.",
            }
        return {
            "status": "not_ready",
            "model_loaded": False,
            "model_name": None,
            "model_version": None,
            "target_unit": None,
            "details": self.predictor.load_error or "Model not loaded.",
        }


# Global prediction service instance
prediction_service = PredictionService()

"""
Inference services package for PropValueAI ML Inference Service.
"""

from ml.inference.services.prediction_service import (
    PredictionService,
    prediction_service,
)

__all__ = ["PredictionService", "prediction_service"]

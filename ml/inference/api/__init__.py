"""
API routing and schema package for PropValueAI ML Inference Service.
"""

from ml.inference.api.schema import (
    PropertyPredictRequest,
    PropertyBatchPredictRequest,
    PropertyPredictResponse,
    PropertyBatchPredictResponse,
    HealthLiveResponse,
    HealthReadyResponse,
    ModelInfoResponse,
)

__all__ = [
    "PropertyPredictRequest",
    "PropertyBatchPredictRequest",
    "PropertyPredictResponse",
    "PropertyBatchPredictResponse",
    "HealthLiveResponse",
    "HealthReadyResponse",
    "ModelInfoResponse",
]

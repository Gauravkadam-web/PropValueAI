"""
FastAPI route definitions for the PropValueAI ML Inference Service.

Exposes endpoints for property price prediction, health checks, and architectural metadata.
Decoupled from application persistence, authentication, and database access.
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ml.inference.config.settings import settings
from ml.inference.services.prediction_service import prediction_service
from ml.inference.api.schema import (
    HealthLiveResponse,
    HealthReadyResponse,
    ModelInfoResponse,
    PropertyBatchPredictRequest,
    PropertyBatchPredictResponse,
    PropertyPredictRequest,
    PropertyPredictResponse,
)

router = APIRouter()


# ==============================================================================
# Health & Status Endpoints
# ==============================================================================

@router.get(
    "/health/live",
    response_model=HealthLiveResponse,
    summary="Liveness check",
    tags=["Health"],
)
async def health_live() -> HealthLiveResponse:
    """Confirms that the FastAPI process is active and accepting HTTP requests."""
    return HealthLiveResponse(
        status="alive",
        service=settings.app_name,
    )


@router.get(
    "/health/ready",
    response_model=HealthReadyResponse,
    summary="Readiness check",
    tags=["Health"],
    responses={
        200: {"description": "Service is ready and model is loaded"},
        503: {"description": "Service is not ready — model artifact missing or failed to load"},
    },
)
async def health_ready():
    """Reports whether the model artifact is loaded and ready for inference."""
    readiness = prediction_service.get_readiness()
    if not readiness["model_loaded"]:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=readiness,
        )

    return HealthReadyResponse(**readiness)


# ==============================================================================
# Prediction Endpoints
# ==============================================================================

@router.post(
    f"{settings.api_prefix}/predict",
    response_model=PropertyPredictResponse,
    summary="Predict single property price",
    tags=["Inference"],
    responses={
        200: {"description": "Successful prediction in Lakhs INR"},
        422: {"description": "Validation error in property features"},
        503: {"description": "Model is not loaded or ready"},
    },
)
async def predict_single(property_req: PropertyPredictRequest) -> PropertyPredictResponse:
    """
    Accepts validated property characteristics and returns the predicted price
    in Lakhs of Indian Rupees (1 Lakh = ₹100,000) using the fitted pipeline.
    """
    result = prediction_service.predict_single(property_req.to_feature_dict())
    return PropertyPredictResponse(**result)


@router.post(
    f"{settings.api_prefix}/predict/batch",
    response_model=PropertyBatchPredictResponse,
    summary="Predict prices for a batch of properties",
    tags=["Inference"],
    responses={
        200: {"description": "Successful batch predictions matching input order"},
        422: {"description": "Validation error or batch size exceeded"},
        503: {"description": "Model is not loaded or ready"},
    },
)
async def predict_batch(batch_req: PropertyBatchPredictRequest) -> PropertyBatchPredictResponse:
    """
    Accepts up to 100 properties and returns ordered predictions in Lakhs INR.
    """
    count = len(batch_req.properties)
    if count > settings.max_batch_size:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Batch size {count} exceeds maximum allowed limit of {settings.max_batch_size}.",
        )

    feature_dicts = [p.to_feature_dict() for p in batch_req.properties]
    result = prediction_service.predict_batch(feature_dicts)
    return PropertyBatchPredictResponse(**result)


# ==============================================================================
# Model Info & Root Endpoints
# ==============================================================================

@router.get(
    f"{settings.api_prefix}/model-info",
    response_model=ModelInfoResponse,
    summary="Retrieve model architecture and metadata",
    tags=["Metadata"],
)
async def get_model_info() -> ModelInfoResponse:
    """Returns verified model metadata, feature schemas, and educational disclaimer."""
    info = prediction_service.get_model_info()
    return ModelInfoResponse(**info)


@router.get(
    "/",
    summary="Root service status",
    tags=["Health"],
)
async def root():
    """Returns basic service descriptor and documentation link."""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "documentation": "/docs",
        "disclaimer": settings.disclaimer,
    }

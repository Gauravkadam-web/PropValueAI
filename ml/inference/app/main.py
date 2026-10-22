"""
FastAPI ML Inference Service for PropValueAI.

Provides standalone endpoints for property price prediction, model health,
and architectural metadata. Decoupled from application persistence and auth.
"""

import logging
import uuid
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ml.inference.app.config import settings
from ml.inference.app.predictor import InferenceError, ModelNotReadyError, predictor
from ml.inference.app.schemas import (
    HealthLiveResponse,
    HealthReadyResponse,
    ModelInfoResponse,
    PropertyBatchPredictRequest,
    PropertyBatchPredictResponse,
    PropertyPredictRequest,
    PropertyPredictResponse,
)

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("propvalueai.inference")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager: loads model once at startup."""
    logger.info("Initializing PropValueAI Inference Service...")
    success = predictor.load_model()
    if not success:
        logger.warning(
            f"Model artifact could not be loaded at startup: {predictor.load_error}. "
            f"Readiness check will report 503 until resolved."
        )
    else:
        logger.info(
            f"Ready for inference. Loaded {predictor.model_name} (v{predictor.model_version}) "
            f"predicting in {predictor.target_unit}."
        )
    yield
    logger.info("Shutting down PropValueAI Inference Service.")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Internal ML Inference Service for PropValueAI Real Estate Price Prediction. "
        "Provides simulated property valuations for educational demonstration purposes only."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ==============================================================================
# Error Handlers
# ==============================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Formats validation errors cleanly without exposing internals or stack traces."""
    errors = []
    for err in exc.errors():
        field_loc = " -> ".join(str(loc) for loc in err.get("loc", []))
        msg = err.get("msg", "Invalid value")
        errors.append({"field": field_loc, "message": msg})
    logger.warning(f"Validation failure on {request.method} {request.url.path}: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "The submitted property request failed input validation.",
            "details": errors,
        },
    )


@app.exception_handler(ModelNotReadyError)
async def model_not_ready_handler(request: Request, exc: ModelNotReadyError):
    """Returns 503 Service Unavailable when inference is requested before model is ready."""
    logger.error(f"Inference rejected — model not ready: {exc}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Service Unavailable",
            "message": "Inference service is currently not ready to handle prediction requests.",
            "details": str(exc),
        },
    )


@app.exception_handler(InferenceError)
async def inference_error_handler(request: Request, exc: InferenceError):
    """Returns 500 when an internal pipeline transformation failure occurs."""
    logger.error(f"Inference computation error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Inference Failure",
            "message": "An error occurred while computing the property price prediction.",
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Safeguard: catches unexpected runtime exceptions without exposing stack traces."""
    logger.error(f"Unhandled server error on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact the system administrator.",
        },
    )


# ==============================================================================
# Health & Status Endpoints
# ==============================================================================

@app.get(
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


@app.get(
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
    if not predictor.is_ready:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "model_loaded": False,
                "model_name": None,
                "model_version": None,
                "target_unit": None,
                "details": predictor.load_error or "Model artifact has not been initialized.",
            },
        )

    return HealthReadyResponse(
        status="ready",
        model_loaded=True,
        model_name=predictor.model_name,
        model_version=predictor.model_version,
        target_unit=predictor.target_unit,
        details="Fitted pipeline is active and ready for inference requests.",
    )


# ==============================================================================
# Prediction Endpoints
# ==============================================================================

@app.post(
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
    prediction_id = str(uuid.uuid4())
    predicted_val = predictor.predict_single(property_req.to_feature_dict())

    return PropertyPredictResponse(
        prediction_id=prediction_id,
        predicted_price=predicted_val,
        target_unit=predictor.target_unit,
        model_name=predictor.model_name,
        model_version=predictor.model_version,
        disclaimer=settings.disclaimer,
    )


@app.post(
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
    predictions_raw = predictor.predict_batch(feature_dicts)

    responses = [
        PropertyPredictResponse(
            prediction_id=str(uuid.uuid4()),
            predicted_price=val,
            target_unit=predictor.target_unit,
            model_name=predictor.model_name,
            model_version=predictor.model_version,
            disclaimer=settings.disclaimer,
        )
        for val in predictions_raw
    ]

    return PropertyBatchPredictResponse(
        predictions=responses,
        count=count,
        model_name=predictor.model_name,
        model_version=predictor.model_version,
        disclaimer=settings.disclaimer,
    )


# ==============================================================================
# Model Info Endpoint
# ==============================================================================

@app.get(
    f"{settings.api_prefix}/model-info",
    response_model=ModelInfoResponse,
    summary="Retrieve model architecture and metadata",
    tags=["Metadata"],
)
async def get_model_info() -> ModelInfoResponse:
    """Returns verified model metadata, feature schemas, and educational disclaimer."""
    return ModelInfoResponse(
        model_name=predictor.model_name,
        model_version=predictor.model_version,
        target_variable=predictor.metadata.get("target_variable", "price"),
        target_unit=predictor.target_unit,
        feature_schema=predictor.metadata.get("feature_schema", {
            "input_features": ["total_sqft", "size", "bath", "balcony", "area_type"],
            "dropped_features": ["society", "site_location", "availability"],
        }),
        evaluation_metrics=predictor.metadata.get("evaluation_metrics", {}),
        limitations=predictor.metadata.get("limitations", settings.disclaimer),
    )


@app.get(
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

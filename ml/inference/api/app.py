"""
FastAPI application factory and lifecycle manager for PropValueAI ML Inference Service.

Configures lifespan startup/shutdown, standardized error handlers, and attaches routes.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ml.inference.config.settings import settings
from ml.inference.model.loader import ModelNotReadyError
from ml.inference.model.predictor import InferenceError, predictor
from ml.inference.api.routes import router

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("propvalueai.inference")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager: loads model artifact once at startup."""
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


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
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
        """Returns 500 Internal Server Error when inference execution fails."""
        logger.error(f"Prediction pipeline failure: {exc}", exc_info=True)
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

    # Attach all routes
    app.include_router(router)
    return app


# Default app instance
app = create_app()

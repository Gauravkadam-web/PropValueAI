"""
Configuration settings for the PropValueAI ML Inference Service.

Resolves model artifact and metadata locations independently of the working directory,
and supports environment variable overrides.
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass


# Determine project root and ml directories reliably
CURRENT_FILE = Path(__file__).resolve()
# ml/inference/app/config.py -> app (parent) -> inference (parent) -> ml (parent) -> project_root (parent)
APP_DIR = CURRENT_FILE.parent
INFERENCE_DIR = APP_DIR.parent
ML_DIR = INFERENCE_DIR.parent
PROJECT_ROOT = ML_DIR.parent

# Ensure project root is present on sys.path for unpickling custom transformers
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@dataclass(frozen=True)
class Settings:
    """Inference service configuration settings."""

    app_name: str = "PropValueAI ML Inference Service"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"

    # Default artifact paths relative to ml/inference/artifacts
    default_artifact_dir: Path = INFERENCE_DIR / "artifacts"
    model_path: Path = Path(
        os.environ.get("PROPVALUEAI_MODEL_PATH")
        or os.environ.get("MODEL_PATH")
        or (INFERENCE_DIR / "artifacts" / "model.joblib")
    ).resolve()

    metadata_path: Path = Path(
        os.environ.get("PROPVALUEAI_METADATA_PATH")
        or os.environ.get("METADATA_PATH")
        or (INFERENCE_DIR / "artifacts" / "metadata.json")
    ).resolve()

    # Network settings
    host: str = os.environ.get("PROPVALUEAI_HOST", os.environ.get("HOST", "127.0.0.1"))
    port: int = int(os.environ.get("PROPVALUEAI_PORT", os.environ.get("PORT", "8000")))

    # Validation thresholds
    max_batch_size: int = int(os.environ.get("PROPVALUEAI_MAX_BATCH_SIZE", "100"))
    log_level: str = os.environ.get("PROPVALUEAI_LOG_LEVEL", "INFO").upper()

    # Educational Disclaimer
    disclaimer: str = (
        "PropValueAI provides simulated estimates for educational demonstration purposes only. "
        "Predictions are not actual Pune market valuations."
    )


settings = Settings()

"""
Entry point for the PropValueAI ML Inference Service.

Allows starting the service either via:
  uvicorn ml.inference.main:app --host 127.0.0.1 --port 8000
or directly:
  python ml/inference/main.py
"""

import uvicorn
from ml.inference.config.settings import settings
from ml.inference.api.app import app

if __name__ == "__main__":
    uvicorn.run(
        "ml.inference.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )

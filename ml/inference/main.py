"""
Entry point for the PropValueAI ML Inference Service.

Allows starting the service either via:
  uvicorn ml.inference.app.main:app --host 127.0.0.1 --port 8000
or directly:
  python ml/inference/main.py
"""

import uvicorn
from ml.inference.app.config import settings
from ml.inference.app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "ml.inference.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )

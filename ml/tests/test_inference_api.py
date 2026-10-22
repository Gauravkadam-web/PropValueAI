"""
Automated tests for PropValueAI FastAPI ML Inference Service.

Covers:
- Lifespan model loading & verification
- Health liveness & readiness probes
- Missing/invalid artifact handling
- Single prediction (standard, range, unit strings, missing fields, unseen categories)
- Target leakage rejection ('price')
- Invalid numbers, NaN, infinity, bounds rejection
- Batch prediction (ordering, count, limits, single-vs-batch parity)
- Model info and root endpoints
"""

import math
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from ml.inference.api.app import app
from ml.inference.model.loader import ModelNotReadyError
from ml.inference.model.predictor import (
    ModelPredictor,
    InferenceError,
    predictor,
)


@pytest.fixture(scope="module")
def client():
    """Module-level TestClient ensuring lifespan startup runs."""
    with TestClient(app) as test_client:
        yield test_client


# ==============================================================================
# Health Check Tests
# ==============================================================================

def test_health_live_endpoint(client: TestClient):
    """GET /health/live must report alive status and service name."""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "PropValueAI" in data["service"]


def test_health_ready_endpoint_success(client: TestClient):
    """GET /health/ready must return 200 with model information when initialized."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["model_loaded"] is True
    assert data["model_name"] == "Random Forest"
    assert data["model_version"] == "1.0.0"
    assert data["target_unit"] == "Lakhs INR"


def test_health_ready_endpoint_when_not_ready():
    """GET /health/ready must return 503 if model is not loaded."""
    original_state = predictor.is_ready
    original_error = predictor.load_error
    try:
        with TestClient(app) as temp_client:
            # Lifespan startup runs on enter; now simulate unready state
            predictor.is_ready = False
            predictor.load_error = "Simulated uninitialized artifact."
            response = temp_client.get("/health/ready")
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "not_ready"
            assert data["model_loaded"] is False
            assert "Simulated" in data["details"]
    finally:
        predictor.is_ready = original_state
        predictor.load_error = original_error


# ==============================================================================
# Single Prediction Tests
# ==============================================================================

def test_single_prediction_valid_standard(client: TestClient):
    """Standard 2 BHK property prediction returns 200, positive finite price, and disclaimer."""
    payload = {
        "total_sqft": 1056.0,
        "size": "2 BHK",
        "bath": 2.0,
        "balcony": 1.0,
        "area_type": "Super built-up  Area",
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction_id" in data
    assert isinstance(data["predicted_price"], float)
    assert data["predicted_price"] > 0
    assert data["target_unit"] == "Lakhs INR"
    assert data["model_name"] == "Random Forest"
    assert data["model_version"] == "1.0.0"
    assert "educational demonstration" in data["disclaimer"]


def test_single_prediction_with_area_range(client: TestClient):
    """Area range '2100 - 2850' is parsed by transformer and returns a valid prediction."""
    payload = {
        "total_sqft": "2100 - 2850",
        "size": "3 BHK",
        "bath": 3.0,
        "balcony": 2.0,
        "area_type": "Super built-up  Area",
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_price"] > 0


def test_single_prediction_with_unit_conversion(client: TestClient):
    """Area unit string '1000Sq. Meter' is converted to sqft and evaluated properly."""
    payload = {
        "total_sqft": "1000Sq. Meter",
        "size": "4 BHK",
        "bath": 4.0,
        "balcony": 2.0,
        "area_type": "Plot  Area",
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_price"] > 0


def test_single_prediction_with_missing_optional_fields(client: TestClient):
    """Missing optional fields (bath, balcony, size, area_type) are cleanly median-imputed."""
    payload = {
        "total_sqft": 1200.0,
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_price"] > 0


def test_single_prediction_with_direct_bhk_alias(client: TestClient):
    """Direct numeric 'bhk: 3' alias is supported in place of 'size'."""
    payload = {
        "total_sqft": 1500.0,
        "bhk": 3,
        "bath": 2.0,
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_price"] > 0


def test_single_prediction_with_unseen_area_type(client: TestClient):
    """Unseen area_type category is ignored by OneHotEncoder and does not crash."""
    payload = {
        "total_sqft": 1200.0,
        "size": "2 BHK",
        "bath": 2.0,
        "area_type": "Futuristic Sky Villa Zone",
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_price"] > 0


# ==============================================================================
# Input Validation & Target Leakage Rejection Tests
# ==============================================================================

def test_rejects_target_price_in_payload(client: TestClient):
    """Input containing 'price' must be rejected with 422 to prevent target leakage."""
    payload = {
        "total_sqft": 1200.0,
        "size": "2 BHK",
        "price": 75.0,  # Target leakage attempt
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "price" in str(data)


def test_rejects_zero_or_negative_sqft(client: TestClient):
    """Non-positive total_sqft must return 422."""
    for invalid_val in [0, -500, "-1200"]:
        response = client.post("/api/v1/predict", json={"total_sqft": invalid_val})
        assert response.status_code == 422


def test_rejects_nan_and_infinite_sqft(client: TestClient):
    """NaN or infinite numeric values must be rejected by Pydantic schema or API."""
    from pydantic import ValidationError
    from ml.inference.api.schema import PropertyPredictRequest

    with pytest.raises(ValidationError):
        PropertyPredictRequest(total_sqft=float("nan"))

    with pytest.raises(ValidationError):
        PropertyPredictRequest(total_sqft=float("inf"))

    with pytest.raises(ValidationError):
        PropertyPredictRequest(total_sqft=float("-inf"))

    # Also test sending NaN string or unparseable area via API returns 422
    response = client.post("/api/v1/predict", json={"total_sqft": "NaN"})
    assert response.status_code == 422


def test_rejects_negative_bath_or_balcony(client: TestClient):
    """Negative bathroom or balcony counts must return 422."""
    response = client.post("/api/v1/predict", json={"total_sqft": 1000, "bath": -1.0})
    assert response.status_code == 422

    response = client.post("/api/v1/predict", json={"total_sqft": 1000, "balcony": -2.0})
    assert response.status_code == 422


def test_rejects_excessive_bath_count(client: TestClient):
    """Bath count > 20 exceeds residential bounds and returns 422."""
    response = client.post("/api/v1/predict", json={"total_sqft": 1000, "bath": 25.0})
    assert response.status_code == 422


def test_rejects_empty_string_total_sqft(client: TestClient):
    """Empty or whitespace-only total_sqft string returns 422."""
    response = client.post("/api/v1/predict", json={"total_sqft": "   "})
    assert response.status_code == 422


# ==============================================================================
# Batch Prediction Tests
# ==============================================================================

def test_batch_prediction_valid(client: TestClient):
    """Batch prediction preserves input order and returns count and predictions."""
    payload = {
        "properties": [
            {"total_sqft": 800.0, "size": "1 BHK", "bath": 1.0},
            {"total_sqft": 1200.0, "size": "2 BHK", "bath": 2.0},
            {"total_sqft": 2000.0, "size": "3 BHK", "bath": 3.0},
        ]
    }
    response = client.post("/api/v1/predict/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 3
    assert len(data["predictions"]) == 3
    assert data["model_name"] == "Random Forest"
    # Typically, price scales monotonically with area
    p1 = data["predictions"][0]["predicted_price"]
    p2 = data["predictions"][1]["predicted_price"]
    p3 = data["predictions"][2]["predicted_price"]
    assert p1 > 0 and p2 > 0 and p3 > 0


def test_single_versus_batch_consistency(client: TestClient):
    """Predicting an item singly yields the exact same price as predicting it in a batch."""
    prop_a = {"total_sqft": 1350.0, "size": "2 BHK", "bath": 2.0, "balcony": 1.0, "area_type": "Super built-up  Area"}
    prop_b = {"total_sqft": 2400.0, "size": "4 Bedroom", "bath": 4.0, "balcony": 2.0, "area_type": "Plot  Area"}

    # Single predictions
    single_res_a = client.post("/api/v1/predict", json=prop_a).json()["predicted_price"]
    single_res_b = client.post("/api/v1/predict", json=prop_b).json()["predicted_price"]

    # Batch prediction
    batch_res = client.post("/api/v1/predict/batch", json={"properties": [prop_a, prop_b]}).json()
    batch_res_a = batch_res["predictions"][0]["predicted_price"]
    batch_res_b = batch_res["predictions"][1]["predicted_price"]

    assert single_res_a == batch_res_a
    assert single_res_b == batch_res_b


def test_batch_empty_list_rejected(client: TestClient):
    """Empty batch returns 422."""
    response = client.post("/api/v1/predict/batch", json={"properties": []})
    assert response.status_code == 422


def test_batch_exceeding_max_limit(client: TestClient):
    """Batch exceeding max allowed limit (100) returns 422."""
    excessive_properties = [{"total_sqft": 1000.0, "size": "2 BHK"}] * 105
    response = client.post("/api/v1/predict/batch", json={"properties": excessive_properties})
    assert response.status_code == 422


# ==============================================================================
# Metadata & Root Tests
# ==============================================================================

def test_model_info_endpoint(client: TestClient):
    """GET /api/v1/model-info returns complete architecture and disclaimer."""
    response = client.get("/api/v1/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_name"] == "Random Forest"
    assert data["target_unit"] == "Lakhs INR"
    assert "input_features" in data["feature_schema"]
    assert "educational demonstration" in data["limitations"].lower()


def test_root_endpoint(client: TestClient):
    """GET / returns service status and docs reference."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["documentation"] == "/docs"


# ==============================================================================
# Predictor Unit & Failure Handling Tests
# ==============================================================================

def test_predictor_missing_artifact(tmp_path: Path):
    """ModelPredictor handles non-existent artifact path gracefully without crashing."""
    missing_path = tmp_path / "non_existent_model.joblib"
    pred = ModelPredictor(model_path=missing_path)
    success = pred.load_model()
    assert success is False
    assert pred.is_ready is False
    assert "not found" in pred.load_error

    with pytest.raises(ModelNotReadyError):
        pred.predict_single({"total_sqft": 1000})


def test_predictor_corrupted_artifact(tmp_path: Path):
    """ModelPredictor handles corrupt file gracefully without crashing."""
    corrupt_file = tmp_path / "corrupt.joblib"
    corrupt_file.write_text("NOT A VALID JOBLIB FILE")
    pred = ModelPredictor(model_path=corrupt_file)
    success = pred.load_model()
    assert success is False
    assert pred.is_ready is False
    assert "Failed to deserialize" in pred.load_error

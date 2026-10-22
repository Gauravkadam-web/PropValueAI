# PropValueAI — ML Inference Service (FastAPI)

**Status:** Phase 3 Complete — Production-Ready Local Inference Service.

The PropValueAI Inference Service is a high-performance, standalone FastAPI service that loads the fitted scikit-learn pipeline (`RandomForestRegressor` + `PropertyFeatureTransformer`) and serves price predictions in Lakhs of Indian Rupees (1 Lakh = ₹100,000).

> [!IMPORTANT]
> **Educational Demonstration Notice:**
> The underlying model is trained on benchmark real-estate data with mapped Pune locality names for educational demonstration purposes. Predictions represent simulated estimates and **must not** be used as certified cadastral or legal real-estate valuations in Pune.

---

## 1. Architecture & Service Boundaries

- **Decoupled Responsibilities:**
  - This service is responsible exclusively for model loading, schema validation, and inference computation.
  - It does **not** handle user authentication, persistence, PostgreSQL access, or prediction history tracking (these belong to Spring Boot in Phase 4).
  - Next.js browser clients will communicate with Spring Boot, which orchestrates backend business logic and queries this internal inference service.
- **Lifespan Initialization:**
  - The model artifact (`ml/inference/artifacts/model.joblib`) and metadata (`ml/inference/artifacts/metadata.json`) are loaded **once** at application startup, not per request.
  - If the artifact is missing or corrupted, the service starts safely but reports `503 Service Unavailable` on `/health/ready` and prediction endpoints.

---

## 2. Directory Layout

```text
ml/inference/
├── model/
│   ├── loader.py            # Artifact deserialization & verification
│   └── predictor.py         # Prediction engine with non-negative guarantee
├── preprocessing/
│   └── preprocess.py        # Inference input DataFrame preparation
├── services/
│   └── prediction_service.py # Business orchestration & disclaimer attachment
├── config/
│   └── settings.py          # Environment-driven settings & CWD-independent path resolution
├── api/
│   ├── app.py               # FastAPI application factory & error handlers
│   ├── routes.py            # Route endpoint definitions
│   └── schema.py            # Pydantic v2 request/response schemas & data validation
├── artifacts/
│   ├── model.joblib         # Fitted Pipeline artifact (Git-tracked)
│   ├── metadata.json        # Architectural metadata & evaluation metrics (Git-tracked)
│   └── .gitkeep
├── requirements.txt         # Inference service dependencies
├── main.py                  # CLI startup entry point
└── README.md                # This documentation
```

---

## 3. Configuration & Environment Overrides

All settings support environment variable overrides:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `PROPVALUEAI_MODEL_PATH` / `MODEL_PATH` | `ml/inference/artifacts/model.joblib` | Absolute or relative path to fitted model artifact |
| `PROPVALUEAI_METADATA_PATH` / `METADATA_PATH` | `ml/inference/artifacts/metadata.json` | Path to model metadata JSON file |
| `PROPVALUEAI_HOST` / `HOST` | `127.0.0.1` | Network binding interface |
| `PROPVALUEAI_PORT` / `PORT` | `8000` | Port for Uvicorn HTTP server |
| `PROPVALUEAI_MAX_BATCH_SIZE` | `100` | Maximum allowed properties in a batch request |
| `PROPVALUEAI_LOG_LEVEL` | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

## 4. API Endpoints

### 4.1 `GET /health/live`
Confirms the FastAPI server process is active.
- **Status:** `200 OK`
- **Response:**
  ```json
  {
    "status": "alive",
    "service": "PropValueAI ML Inference Service"
  }
  ```

### 4.2 `GET /health/ready`
Reports whether the fitted scikit-learn model artifact is loaded and verified for inference.
- **Status:** `200 OK` (when model is loaded) or `503 Service Unavailable` (if model failed to load)
- **Response (200 OK):**
  ```json
  {
    "status": "ready",
    "model_loaded": true,
    "model_name": "Random Forest",
    "model_version": "1.0.0",
    "target_unit": "Lakhs INR",
    "details": "Fitted pipeline is active and ready for inference requests."
  }
  ```

### 4.3 `POST /api/v1/predict`
Accepts a single property's characteristics and returns estimated price in Lakhs INR.

- **Request Headers:** `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "total_sqft": 1056.0,
    "size": "2 BHK",
    "bath": 2.0,
    "balcony": 1.0,
    "area_type": "Super built-up  Area"
  }
  ```
  *Supported variations:*
  - `total_sqft` accepts numeric floats/ints (`1056`), range strings (`"2100 - 2850"`), or unit strings (`"1000Sq. Meter"`, `"1Acres"`).
  - `size` accepts strings (`"2 BHK"`, `"3 Bedroom"`, `"1 RK"`) or integers (`2`). Alternatively, pass `"bhk": 2`.
  - `bath`, `balcony`, `size`, `area_type` are optional (imputed with training medians/modes if omitted).
  - Target variable `price` is strictly forbidden in the request (returns 422 if submitted).

- **Response (200 OK):**
  ```json
  {
    "prediction_id": "98173fc5-ffeb-4373-8167-8e9d29d9ccaf",
    "predicted_price": 55.20,
    "target_unit": "Lakhs INR",
    "model_name": "Random Forest",
    "model_version": "1.0.0",
    "disclaimer": "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."
  }
  ```

### 4.4 `POST /api/v1/predict/batch`
Accepts a batch of up to 100 properties and returns ordered predictions.

- **Request Body:**
  ```json
  {
    "properties": [
      {
        "total_sqft": 800.0,
        "size": "1 BHK",
        "bath": 1.0
      },
      {
        "total_sqft": 1500.0,
        "size": "3 BHK",
        "bath": 2.0
      }
    ]
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "predictions": [
      {
        "prediction_id": "...",
        "predicted_price": 42.15,
        "target_unit": "Lakhs INR",
        "model_name": "Random Forest",
        "model_version": "1.0.0",
        "disclaimer": "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."
      },
      {
        "prediction_id": "...",
        "predicted_price": 89.50,
        "target_unit": "Lakhs INR",
        "model_name": "Random Forest",
        "model_version": "1.0.0",
        "disclaimer": "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."
      }
    ],
    "count": 2,
    "model_name": "Random Forest",
    "model_version": "1.0.0",
    "disclaimer": "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."
  }
  ```

### 4.5 `GET /api/v1/model-info`
Returns architectural metadata, evaluation metrics, and limitations.

---

## 5. Local Setup & Execution Guide (Windows PowerShell)

No Docker or external databases required. Because `model.joblib` and `metadata.json` are committed to Git in `ml/inference/artifacts/`, a fresh clone can run inference immediately without downloading or preprocessing the raw training dataset.

### 1. Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Inference Dependencies (if not already installed)
```powershell
pip install -r ml/inference/requirements.txt
```

### 3. Start the FastAPI Service
```powershell
# Option A: via Uvicorn
uvicorn ml.inference.main:app --host 127.0.0.1 --port 8000 --reload

# Option B: via main.py entry point
python ml/inference/main.py
```

### 4. Open Swagger UI & Documentation
Open in browser:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 5. Check Health Endpoints via PowerShell
```powershell
# Check liveness
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health/live" -Method Get

# Check readiness
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health/ready" -Method Get
```

### 6. Submit Sample Prediction via PowerShell
```powershell
$body = @{
    total_sqft = 1056.0
    size = "2 BHK"
    bath = 2.0
    balcony = 1.0
    area_type = "Super built-up  Area"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/predict" -Method Post -Body $body -ContentType "application/json"
```

### 7. Run Automated Tests
```powershell
pytest ml/tests/test_inference_api.py -v
```
To run all ML tests (37 unit & integration tests):
```powershell
pytest ml/tests/ -v
```

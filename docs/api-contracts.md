# API Contracts — PropValueAI

**Status:** Phase 3 Implemented (FastAPI Inference Service); Spring Boot & Frontend API Contracts in design.

---

## 1. Service Boundaries

### Browser → Spring Boot
The Next.js browser client communicates with Spring Boot application APIs (`/api/properties`, `/api/predictions`, `/api/auth`). It must not access PostgreSQL directly or call the internal FastAPI service directly.

### Spring Boot → FastAPI
Spring Boot calls the internal FastAPI inference service using server-to-server HTTP POST requests. The request must match the feature contract established by the fitted scikit-learn pipeline.

### Spring Boot → PostgreSQL
Spring Boot owns application database access, Flyway migrations, and persistence for users, roles, prediction history, and property bookmarks.

---

## 2. Implemented FastAPI Inference Endpoints (Phase 3)

The internal Python FastAPI inference service exposes the following endpoints:

| Method | Path | Purpose | Status |
|---|---|---|---|
| GET | `/health/live` | Process liveness check | **Implemented** |
| GET | `/health/ready` | Model artifact readiness probe (200 when loaded, 503 if unavailable) | **Implemented** |
| GET | `/api/v1/model-info` | Exposes verified model metadata and limitations | **Implemented** |
| POST | `/api/v1/predict` | Single property price prediction in Lakhs INR | **Implemented** |
| POST | `/api/v1/predict/batch` | Batch property price prediction (1–100 items) | **Implemented** |

---

## 3. Implemented Inference Schemas

### 3.1 `POST /api/v1/predict` (Single Prediction)

#### Request Schema:
```json
{
  "total_sqft": 1056.0,
  "size": "2 BHK",
  "bath": 2.0,
  "balcony": 1.0,
  "area_type": "Super built-up  Area"
}
```

**Field Rules:**
- `total_sqft` (Required): Accepts numeric (`1056`, `1056.0`), range strings (`"2100 - 2850"`), or recognized units (`"1000Sq. Meter"`, `"1Acres"`, `"24Guntha"`, `"10Perch"`, `"500Cents"`). Must be finite and strictly positive (> 0).
- `size` (Optional): Bedroom specification string (`"2 BHK"`, `"3 Bedroom"`, `"1 RK"`) or integer bedroom count (`2`). Alternatively, `"bhk"` can be passed.
- `bath` (Optional): Bathroom count (float or int). Must be $\ge 0$ and $\le 20$. Imputed with training median (2.0) if omitted.
- `balcony` (Optional): Balcony count (float or int). Must be $\ge 0$ and $\le 10$. Imputed with training median (2.0) if omitted.
- `area_type` (Optional): String category (`"Super built-up  Area"`, `"Plot  Area"`, `"Built-up  Area"`, `"Carpet  Area"`). Unseen categories are safely ignored by OneHotEncoder.
- `price` (Forbidden): Must **not** be included; rejected with 422 to prevent target leakage.

#### Response Schema (200 OK):
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

---

### 3.2 `POST /api/v1/predict/batch` (Batch Prediction)

#### Request Schema:
```json
{
  "properties": [
    {
      "total_sqft": 800.0,
      "size": "1 BHK",
      "bath": 1.0
    },
    {
      "total_sqft": 1600.0,
      "size": "3 BHK",
      "bath": 2.0
    }
  ]
}
```
*Constraint: Minimum 1 item, maximum 100 items per batch.*

#### Response Schema (200 OK):
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
      "predicted_price": 84.70,
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

---

## 4. Error Responses

All error responses return structured JSON without leaking stack traces or internal server paths:

- **422 Unprocessable Entity:** Input validation failure (missing required field, unparseable area, target `price` supplied, or negative numbers).
  ```json
  {
    "error": "Validation Error",
    "message": "The submitted property request failed input validation.",
    "details": [
      {
        "field": "body -> total_sqft",
        "message": "total_sqft string '-1200' cannot be parsed to a positive area."
      }
    ]
  }
  ```
- **503 Service Unavailable:** Model artifact missing or uninitialized.
  ```json
  {
    "error": "Service Unavailable",
    "message": "Inference service is currently not ready to handle prediction requests.",
    "details": "Model artifact not found at path: ..."
  }
  ```
- **500 Internal Server Error:** Unexpected pipeline or runtime error.
  ```json
  {
    "error": "Inference Failure",
    "message": "An error occurred while computing the property price prediction."
  }
  ```

---

## 5. Security & Service Boundaries

- **Internal Service:** The FastAPI inference service is designed to run in a private network or local port accessible only by Spring Boot.
- **No Direct Database Ownership:** FastAPI does not connect to PostgreSQL.
- **Educational Disclaimer:** Every successful prediction payload carries the mandatory educational disclaimer.

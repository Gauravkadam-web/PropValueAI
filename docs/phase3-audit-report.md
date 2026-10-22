# PropValueAI — Phase 3 Independent Audit Report & Review Gate

**Audit Date:** October 22, 2026  
**Auditor:** Independent AI Quality Assurance & Architecture Gatekeeper  
**Audit Target:** Phase 3 — Python FastAPI ML Inference Service  
**Target Repository:** `PropValueAI` (Workspace: `d:\PropValueAI`)  
**Git Commit Audited:** `8e5cb0c` (`feat(ml): implement Phase 2 EDA, training pipeline, tests, and audit documentation`)

---

## 1. Executive Verdict

### **VERDICT: PASS WITH NON-BLOCKING FINDINGS**

The Phase 3 implementation strictly adheres to all architectural boundaries, security policies, and contracts specified in `AGENTS.md` and `docs/api-contracts.md`. The FastAPI service is completely decoupled from application persistence and authentication, loads the fitted Phase 2 pipeline once during lifespan startup, enforces rigorous input validation (including strict rejection of target leakage), accurately predicts prices in Lakhs INR with non-negative guarantees, and includes the mandatory educational disclaimer in all responses.

---

## 2. Files and Contracts Inspected

### 2.1 Project Governance & Contract Documentation
- `AGENTS.md` — Architecture boundaries, Phase discipline, and Git safety rules.
- `README.md` — System overview and repository tree.
- `docs/architecture.md` — Service decoupling (Next.js $\rightarrow$ Spring Boot $\rightarrow$ FastAPI).
- `docs/development-roadmap.md` — Phase 3 deliverables and readiness gates.
- `docs/api-contracts.md` — Implemented FastAPI endpoint contracts and schemas.
- `docs/dataset-validation-report.md` — Educational dataset provenance.
- `docs/model-training-report.md` — Verified model architecture and performance.
- `ml/README.md` & `ml/training/README.md` — ML module status and rules.
- `ml/inference/README.md` — Inference service documentation and PowerShell setup.
- `prompts/phase3.md` — Phase 3 implementation prompt.

### 2.2 Implementation Files
- `ml/inference/app/config.py` — Path resolution, environment variable handling, settings dataclass.
- `ml/inference/app/schemas.py` — Pydantic v2 validation models, area parsing, target price rejection.
- `ml/inference/app/predictor.py` — Model loading, fitted state verification, finite prediction.
- `ml/inference/app/main.py` — FastAPI application, lifespan context manager, error handlers.
- `ml/inference/main.py` — CLI startup wrapper.
- `ml/inference/requirements.txt` — Dependency declarations.
- `ml/tests/test_inference_api.py` — 23 automated tests for FastAPI endpoints.
- `.gitignore` — Exclusion rules for artifacts and environments.

---

## 3. Test Command and Actual Results

The automated test suite was executed against the existing project virtual environment:

```powershell
& ".\.venv\Scripts\pytest.exe" ml/tests/ -v
```

### Actual Command Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.7.0 -- D:\PropValueAI\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\PropValueAI
plugins: anyio-4.15.1
collecting ... collected 37 items

ml/tests/test_inference_api.py::test_health_live_endpoint PASSED         [  2%]
ml/tests/test_inference_api.py::test_health_ready_endpoint_success PASSED [  5%]
ml/tests/test_inference_api.py::test_health_ready_endpoint_when_not_ready PASSED [  8%]
ml/tests/test_inference_api.py::test_single_prediction_valid_standard PASSED [ 10%]
ml/tests/test_inference_api.py::test_single_prediction_with_area_range PASSED [ 13%]
ml/tests/test_inference_api.py::test_single_prediction_with_unit_conversion PASSED [ 16%]
ml/tests/test_inference_api.py::test_single_prediction_with_missing_optional_fields PASSED [ 18%]
ml/tests/test_inference_api.py::test_single_prediction_with_direct_bhk_alias PASSED [ 21%]
ml/tests/test_inference_api.py::test_single_prediction_with_unseen_area_type PASSED [ 24%]
ml/tests/test_inference_api.py::test_rejects_target_price_in_payload PASSED [ 27%]
ml/tests/test_inference_api.py::test_rejects_zero_or_negative_sqft PASSED [ 29%]
ml/tests/test_inference_api.py::test_rejects_nan_and_infinite_sqft PASSED [ 32%]
ml/tests/test_inference_api.py::test_rejects_negative_bath_or_balcony PASSED [ 35%]
ml/tests/test_inference_api.py::test_rejects_excessive_bath_count PASSED [ 37%]
ml/tests/test_inference_api.py::test_rejects_empty_string_total_sqft PASSED [ 40%]
ml/tests/test_inference_api.py::test_batch_prediction_valid PASSED       [ 43%]
ml/tests/test_inference_api.py::test_single_versus_batch_consistency PASSED [ 45%]
ml/tests/test_inference_api.py::test_batch_empty_list_rejected PASSED    [ 48%]
ml/tests/test_inference_api.py::test_batch_exceeding_max_limit PASSED    [ 51%]
ml/tests/test_inference_api.py::test_model_info_endpoint PASSED          [ 54%]
ml/tests/test_inference_api.py::test_root_endpoint PASSED                [ 56%]
ml/tests/test_inference_api.py::test_predictor_missing_artifact PASSED   [ 59%]
ml/tests/test_inference_api.py::test_predictor_corrupted_artifact PASSED [ 62%]
ml/tests/test_predictor.py::test_artifacts_exist PASSED                  [ 64%]
ml/tests/test_predictor.py::test_metadata_schema PASSED                  [ 67%]
ml/tests/test_predictor.py::test_artifact_prediction_consistency PASSED  [ 70%]
ml/tests/test_preprocessing.py::test_area_numeric_parsing PASSED         [ 72%]
ml/tests/test_preprocessing.py::test_area_range_conversion PASSED        [ 75%]
ml/tests/test_preprocessing.py::test_recognized_unit_conversions PASSED  [ 78%]
ml/tests/test_preprocessing.py::test_invalid_and_missing_area_values PASSED [ 81%]
ml/tests/test_bedroom_parsing PASSED              [ 83%]
ml/tests/test_preprocessing.py::test_property_feature_transformer_dataframe PASSED [ 86%]
ml/tests/test_preprocessing.py::test_unseen_categorical_values_in_pipeline PASSED [ 89%]
ml/tests/test_training.py::test_pipeline_output_shape_and_finite_predictions PASSED [ 91%]
ml/tests/test_training.py::test_reproducible_splitting PASSED            [ 94%]
ml/tests/test_training.py::test_training_outlier_filtering_rules PASSED  [ 97%]
ml/tests/test_training.py::test_pipeline_tree_regressor PASSED           [100%]

======================= 37 passed, 9 warnings in 17.31s =======================
```

**Exit Code:** `0` (Success).  
**Counts:** 37 passed, 0 failed, 0 skipped.  
**Warnings:** 9 non-blocking upstream Starlette deprecation warnings (`StarletteDeprecationWarning: Using 'httpx' with 'starlette.testclient' is deprecated; install 'httpx2' instead`).

---

## 4. Categorized Audit Findings

| Finding ID | Severity | Category | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| **FINDING-01** | **None** | Critical Flaws | No architectural violations, target leakage, runtime retraining, or database leaks found. | **PASS** |
| **FINDING-02** | **None** | High Risks | No authentication bypass, shell injection, or arbitrary file loading vulnerabilities. | **PASS** |
| **FINDING-03** | **None** | Medium Issues | No contract inconsistencies or unhandled NaN/infinity crashes. | **PASS** |
| **FINDING-04** | **Low** | Artifact Tracking | Model artifact (`model.joblib`) and metadata (`metadata.json`) are excluded from Git by `.gitignore`. Fresh clones will require local training or artifact provisioning before starting the service. | **NON-BLOCKING** |
| **FINDING-05** | **Low** | Deprecation Notices | Upstream Starlette 1.9.0 deprecation notices when using `TestClient` with `httpx` instead of `httpx2`. | **NON-BLOCKING** |

---

## 5. Detailed Evidence for Audit Findings

### 5.1 Model Loading and Lifecycle Verification
- **CWD Independence:** In `ml/inference/app/config.py`, `CURRENT_FILE.parent.parent / "artifacts" / "model.joblib"` calculates the artifact path relative to the source code file rather than the current working directory.
- **Environment Overrides:** `PROPVALUEAI_MODEL_PATH` and `PROPVALUEAI_METADATA_PATH` are supported via `os.environ.get()` in `config.py`.
- **Single Load per Lifecycle:** In `ml/inference/app/main.py`, `predictor.load_model()` is called exclusively inside the FastAPI `lifespan` context manager during application startup, never inside request handlers.
- **Controlled Unready State:** In `ml/inference/app/predictor.py`, missing or corrupt files cleanly set `self.is_ready = False` and populate `self.load_error`. Verified by `test_predictor_missing_artifact` and `test_predictor_corrupted_artifact`.
- **No Runtime Training:** No training functions (`fit()`, `cross_val_score()`, `GridSearchCV`) exist anywhere in `ml/inference/`.
- **Artifact Preserved:** Timestamp and checksum of `ml/inference/artifacts/model.joblib` (12,877,491 bytes) were inspected and verified unchanged.

### 5.2 Request Validation & Leakage Controls
- **Target Leakage Rejection:** In `ml/inference/app/schemas.py`, `@model_validator(mode="before")` explicitly checks for `"price"` in the payload and raises `ValueError("Target variable 'price' cannot be supplied as an input prediction feature.")`. Verified by `test_rejects_target_price_in_payload`, which returned HTTP `422 Unprocessable Entity`.
- **Area Normalization:** In `ml/inference/app/schemas.py`, strings are validated against `parse_sqft_value()`. Non-positive strings (e.g., `"-1200"`), whitespace-only strings, and empty strings are rejected with HTTP 422.
- **Finiteness & Range Bounds:** Bathroom counts are bounded ($0 \le \text{bath} \le 20$) and balcony counts are bounded ($0 \le \text{balcony} \le 10$). Rejection of NaN, infinite numbers, and excessive bathrooms verified by tests.
- **Missing & Unseen Values:** Missing optional inputs (`bath`, `balcony`, `size`, `area_type`) are imputed by the pipeline's median/most-frequent imputers. Unseen categories (e.g. `"Futuristic Sky Villa Zone"`) are zero-encoded without raising exceptions, verified by `test_single_prediction_with_unseen_area_type`.
- **Batch Enforcing:** Batch request schema `PropertyBatchPredictRequest` enforces `min_length=1`, and `main.py` rejects requests with $> 100$ items before inference starts.

### 5.3 Prediction Semantics & Units
- **Target Unit Consistency:** Predictions are denominated in **Lakhs INR** ($1\text{ Lakh} = ₹100,000$). No accidental extra multiplication by 100,000 was introduced.
- **Non-Negative Guarantee:** In `ml/inference/app/predictor.py`, `clean_val = max(0.0, val)` guarantees non-negative valuations.
- **Educational Disclaimer:** Every response payload from `/api/v1/predict` and `/api/v1/predict/batch` includes:
  > *"PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."*

### 5.4 Endpoint Review
- `GET /health/live`: Returns `200 OK` (`{"status": "alive", "service": "PropValueAI ML Inference Service"}`).
- `GET /health/ready`: Returns `200 OK` when model is loaded; returns `503 Service Unavailable` with explanatory JSON when unready.
- `GET /api/v1/model-info`: Returns model name (`Random Forest`), version (`1.0.0`), target unit (`Lakhs INR`), feature schema, and evaluation metrics loaded from `metadata.json`.
- `POST /api/v1/predict`: Returns `200 OK` with unique `prediction_id`, `predicted_price`, and disclaimer.
- `POST /api/v1/predict/batch`: Returns `200 OK` with ordered predictions and total count. Single-versus-batch prediction consistency was verified identical to 2 decimal places.

---

## 6. Dependencies & Artifact Reproducibility Review

### Dependencies:
`ml/inference/requirements.txt` specifies:
- `fastapi>=0.110.0`
- `uvicorn[standard]>=0.28.0`
- `pydantic>=2.6.0`
- `httpx>=0.27.0`
- `pandas>=2.2.0`
- `numpy>=1.26.0`
- `scikit-learn>=1.4.0`
- `joblib>=1.3.0`

The installed environment contains `fastapi 0.159.1`, `uvicorn 0.54.0`, `pydantic 2.14.1`, `httpx 0.28.1`, `scikit-learn 1.9.1`, and `joblib 1.6.0`. There are zero package conflicts with the existing Phase 2 stack.

### Artifact Exclusion Note (Finding-04):
In `.gitignore`, `ml/inference/artifacts/*` and `*.joblib` prevent tracking binary weights in Git.
- **Current State:** Both `model.joblib` (12.8 MB) and `metadata.json` (2.9 KB) exist locally in `ml/inference/artifacts/`.
- **Reproducibility Assessment:** In future phases (e.g. CI/CD or deployment), the model artifact must either be generated via `python ml/training/scripts/train.py` or fetched from an external artifact store. For local Phase 4 Spring Boot development, the local artifact remains intact and accessible.

---

## 7. Git Safety Confirmation

- Zero files were staged, committed, or pushed by the audit.
- No files were deleted, reset, or stashed.
- The Phase 2 trained model artifact (`ml/inference/artifacts/model.joblib`) was not overwritten or retrained.

---

## 8. Final Recommendation

### **RECOMMENDATION: APPROVE PHASE 3 & PROCEED TO PHASE 4**

Phase 3 is mathematically sound, functionally complete, thoroughly tested (37/37 green), and architecturally compliant. Ready for Phase 4 (Spring Boot Backend Core).

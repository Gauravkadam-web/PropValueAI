# ML Module

**Status:** Phase 3 Complete — FastAPI ML Inference Service implemented and verified.

## Responsibilities
- `training/`: offline dataset inspection, EDA, training, evaluation, and experiment records.
- `inference/`: production-ready FastAPI inference service exposing health checks, model metadata, and single/batch property price prediction endpoints.
- `pipeline/`: optional orchestration modules if needed in future phases.
- `common/`: shared utilities, unit conversion factors, constants, and custom scikit-learn transformers.
- `tests/`: unit and integration tests for preprocessing, training reproducibility, artifact loading, and FastAPI inference API.

## Current Repository Structure

```text
ml/
├── training/
│   ├── data/
│   │   ├── raw/                 # Pune_House_Data.csv (untracked by Git)
│   │   ├── processed/           # Processed datasets (untracked by Git)
│   │   ├── external/            # External references
│   │   └── README.md            # Data storage & provenance rules
│   ├── scripts/
│   │   ├── inspect_dataset.py   # Dataset profiling utility
│   │   ├── eda.py               # Exploratory data analysis & plot generator
│   │   ├── train.py             # 5-fold CV & model training pipeline
│   │   └── evaluate.py          # Standalone artifact evaluation utility
│   ├── experiments/
│   │   └── plots/               # Generated EDA plots (untracked by Git)
│   ├── requirements.txt         # Training dependencies
│   └── README.md                # Training documentation
├── pipeline/
│   ├── __init__.py              # Pipeline package
│   └── pipeline.py              # Reusable ColumnTransformer & Pipeline factory
├── inference/
│   ├── model/
│   │   ├── loader.py            # Artifact loading & verification
│   │   └── predictor.py         # Prediction engine with non-negative guarantee
│   ├── preprocessing/
│   │   └── preprocess.py        # Inference input DataFrame preparation
│   ├── services/
│   │   └── prediction_service.py # Business orchestration & disclaimer attachment
│   ├── config/
│   │   └── settings.py          # Configuration settings & environment overrides
│   ├── api/
│   │   ├── app.py               # FastAPI app factory & error handlers
│   │   ├── routes.py            # Endpoint route definitions
│   │   └── schema.py            # Pydantic v2 request/response schemas
│   ├── artifacts/
│   │   ├── model.joblib         # Fitted Pipeline artifact (Git-tracked)
│   │   └── metadata.json        # Model architecture & evaluation metadata (Git-tracked)
│   ├── requirements.txt         # Inference service dependencies
│   ├── main.py                  # CLI startup entry point
│   └── README.md                # Inference documentation & API guide
├── common/
│   ├── constants.py             # Feature lists, random seed, unit conversions
│   ├── utils.py                 # Parsing and numerical utility functions
│   └── transformers.py          # PropertyFeatureTransformer (scikit-learn compatible)
├── tests/
│   ├── conftest.py              # Pytest environment & path setup
│   ├── test_preprocessing.py    # Unit tests for sqft & bhk parsing, imputations
│   ├── test_training.py         # Unit tests for pipeline shapes & reproducibility
│   ├── test_predictor.py        # Unit tests for artifact loading & predictions
│   └── test_inference_api.py    # Automated integration tests for FastAPI service
├── requirements.txt             # ML shared dependencies
└── README.md
```

## Current Model Artifact & Performance

- **Selected Model:** Random Forest Regressor (`sklearn.ensemble.RandomForestRegressor`)
- **Fitted Pipeline:** Self-contained `PropertyFeatureTransformer` -> `ColumnTransformer` (median imputers, OneHotEncoder) -> `RandomForestRegressor`.
- **5-Fold Cross-Validation Metrics (on 10,015 training observations):**
  - **CV MAE:** 34.97 ± 2.61 Lakhs INR
  - **CV RMSE:** 88.39 ± 8.67 Lakhs INR
  - **CV $R^2$:** 0.6085 ± 0.0280
- **Held-Out Test Set Performance (on 2,508 test observations):**
  - **Test MAE:** 33.26 Lakhs INR
  - **Test RMSE:** 88.74 Lakhs INR
  - **Test $R^2$:** 0.6365
- **Dataset Scope:** Educational demonstration based on CC0 benchmark data with mapped Pune localities. Predictions represent simulated estimates.

## Fresh-Clone Setup Guide

### Option A — Run the Existing Model (Recommended for API & Backend Development)
If you only need to run the FastAPI inference service, you do **not** need to download the raw training dataset because the fitted artifact (`model.joblib`) and metadata (`metadata.json`) are committed to Git in `ml/inference/artifacts/`.

1. **Clone repository:**
   ```powershell
   git clone https://github.com/Gauravkadam-web/PropValueAI.git
   cd PropValueAI
   ```
2. **Create and activate virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. **Install inference dependencies:**
   ```powershell
   pip install -r ml/inference/requirements.txt
   ```
4. **Confirm committed artifacts exist:**
   ```powershell
   Test-Path ml/inference/artifacts/model.joblib
   Test-Path ml/inference/artifacts/metadata.json
   ```
5. **Start the FastAPI inference service:**
   ```powershell
   uvicorn ml.inference.main:app --host 127.0.0.1 --port 8000 --reload
   ```
6. **Verify health & readiness:**
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/health/live" -Method Get
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/health/ready" -Method Get
   ```
7. **Test a sample prediction:**
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

---

### Option B — Regenerate the Model Artifacts (For ML Experimentation & Training)
The raw training dataset is ignored by Git to preserve repository hygiene. If you want to re-run EDA, train alternative estimators, or re-export artifacts:

1. **Obtain the dataset:**
   Acquire `Pune_House_Data.csv` from the approved educational source or project owner.
2. **Place raw dataset at the verified location:**
   Copy the CSV into:
   ```text
   ml/training/data/raw/Pune_House_Data.csv
   ```
3. **Install training dependencies:**
   ```powershell
   pip install -r ml/training/requirements.txt
   ```
4. **Execute training and export pipeline:**
   ```powershell
   python ml/training/scripts/train.py
   ```
   This will execute 80/20 splitting, 5-fold cross-validation, refit the winning Random Forest pipeline, and regenerate both `ml/inference/artifacts/model.joblib` and `ml/inference/artifacts/metadata.json`.
5. **Verify newly generated artifacts:**
   ```powershell
   python ml/training/scripts/evaluate.py --model-path ml/inference/artifacts/model.joblib --data-path ml/training/data/raw/Pune_House_Data.csv
   ```

> [!NOTE]
> **Educational Demonstration Disclaimer:**
> The dataset is derived from the benchmark CC0 real-estate dataset with synthetically substituted Pune locality labels.
> *"PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."*

---

## Running Tests

From project root:
```powershell
pytest ml/tests/ -v
```
All 37 unit and integration tests pass cleanly (100% green).

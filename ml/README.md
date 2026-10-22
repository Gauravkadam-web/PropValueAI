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
├── inference/
│   ├── app/
│   │   ├── __init__.py          # Inference package initialization
│   │   ├── config.py            # Path resolution & settings
│   │   ├── schemas.py           # Pydantic v2 request/response schemas
│   │   ├── predictor.py         # Model loading & inference manager
│   │   └── main.py              # FastAPI application & endpoints
│   ├── artifacts/
│   │   ├── model.joblib         # Fitted Pipeline artifact (untracked by Git)
│   │   └── metadata.json        # Model architecture & evaluation metadata
│   ├── requirements.txt         # Inference service dependencies
│   ├── main.py                  # CLI startup entry point
│   └── README.md                # Inference documentation & API guide
├── common/
│   ├── constants.py             # Feature lists, random seed, unit conversions
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

## Running Tests

From project root:
```powershell
pytest ml/tests/ -v
```
All 37 unit and integration tests pass cleanly (100% green).

# ML Module

**Status:** Phase 2 complete. Offline EDA, preprocessing pipeline, model training, cross-validation, and pipeline artifact export are complete. Inference service (Phase 3) is pending.

## Responsibilities
- `training/`: offline dataset inspection, EDA, training, evaluation, and experiment records.
- `inference/`: holds exported artifacts (`model.joblib`, `metadata.json`); Phase 3 will implement FastAPI inference.
- `pipeline/`: optional orchestration modules if needed in future phases.
- `common/`: shared utilities, unit conversion factors, constants, and custom scikit-learn transformers.
- `tests/`: unit and integration tests for preprocessing, training reproducibility, and artifact loading.

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
│   ├── model/                   # Planned inference loaders/predictors (Phase 3)
│   ├── preprocessing/           # Planned inference preprocessing (Phase 3)
│   ├── services/                # Planned prediction service (Phase 3)
│   ├── artifacts/
│   │   ├── model.joblib         # Fitted Pipeline artifact (untracked by Git)
│   │   └── metadata.json        # Model architecture & evaluation metadata
│   ├── config/                  # Planned runtime configuration (Phase 3)
│   └── main.py                  # Planned FastAPI entry point (Phase 3)
├── common/
│   ├── constants.py             # Feature lists, random seed, unit conversions
│   └── transformers.py          # PropertyFeatureTransformer (scikit-learn compatible)
├── tests/
│   ├── conftest.py              # Pytest environment & path setup
│   ├── test_preprocessing.py    # Unit tests for sqft & bhk parsing, imputations
│   ├── test_training.py         # Unit tests for pipeline shapes & reproducibility
│   └── test_predictor.py        # Unit tests for artifact loading & predictions
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
All 14 unit tests pass cleanly (100% green).

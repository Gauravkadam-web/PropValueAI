# ML Training Submodule

This directory contains offline data inspection, exploratory analysis, preprocessing pipeline design, model training, and evaluation scripts for PropValueAI.

## Directory Structure

```text
ml/training/
├── data/
│   ├── raw/             # Original immutable dataset (Pune_House_Data.csv)
│   ├── processed/       # Prepared/split training data (ignored by Git)
│   ├── external/        # Auxiliary reference data
│   └── README.md        # Data management rules
├── scripts/
│   ├── inspect_dataset.py # CLI dataset profiling tool
│   ├── eda.py             # Exploratory Data Analysis & plot generation
│   ├── train.py           # Leakage-free training & model selection
│   └── evaluate.py        # Standalone artifact evaluation utility
├── experiments/
│   └── plots/           # Generated EDA figures (ignored by Git)
├── requirements.txt     # Training & evaluation dependencies
└── README.md            # Submodule documentation
```

## Raw Dataset Placement (Required for Training Only)

The raw dataset `Pune_House_Data.csv` is excluded from Git to preserve repository hygiene. 
Before running training or EDA scripts on a fresh clone:
1. Obtain `Pune_House_Data.csv` from the approved educational source or project owner.
2. Place it into:
   ```text
   ml/training/data/raw/Pune_House_Data.csv
   ```
*(Note: If you only wish to run the FastAPI inference service, this dataset is NOT required because the trained model artifact is committed to Git).*

## Available Scripts and Commands

All commands should be executed from the project root using the activated virtual environment (`.\.venv\Scripts\python`):

### 1. Dataset Inspection
Profiles raw CSV files (dimensions, missing values, duplicates, numeric statistics, categorical frequencies):
```powershell
python ml/training/scripts/inspect_dataset.py ml/training/data/raw/Pune_House_Data.csv
```

### 2. Exploratory Data Analysis (EDA)
Computes target and feature distributions, audits real-estate domain anomalies, and exports diagnostic plots to `ml/training/experiments/plots/`:
```powershell
python ml/training/scripts/eda.py
```

### 3. Model Training & Pipeline Export
Executes 80/20 train-test split, training-only outlier filtering, 5-fold cross-validation on 5 candidate models, fits the winning Random Forest pipeline, and exports `model.joblib` and `metadata.json` to `ml/inference/artifacts/`:
```powershell
python ml/training/scripts/train.py
```

### 4. Independent Artifact Evaluation
Loads the exported `model.joblib` pipeline and computes MAE, RMSE, and $R^2$ against an evaluation dataset:
```powershell
python ml/training/scripts/evaluate.py --model-path ml/inference/artifacts/model.joblib --data-path ml/training/data/raw/Pune_House_Data.csv
```

## Methodology & Architectural Boundaries

1. **No Online Retraining:** Training is strictly offline. Online prediction services (Phase 3 FastAPI) only load pre-fitted `.joblib` artifacts.
2. **Leakage-Free Transformations:** `train_test_split` is applied before fitting any imputers, scalers, or encoders.
3. **Self-Contained Pipeline:** The exported artifact (`model.joblib`) bundles both feature extraction (`PropertyFeatureTransformer`), preprocessing (`ColumnTransformer`), and the regression model (`RandomForestRegressor`).
4. **Educational Scope:** The dataset is derived from the benchmark CC0 real-estate dataset with mapped Pune locations. Model predictions are estimates for educational demonstration only.

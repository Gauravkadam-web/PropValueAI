# Model Training and Evaluation Report

**Project:** PropValueAI — Real Estate Price Prediction Using Python and Machine Learning  
**Phase:** Phase 2 — EDA, Preprocessing, Model Training & Evaluation  
**Date:** 2026-10-22  
**Target Variable:** `price` (in Lakhs of INR)  
**Selected Model:** Random Forest Regressor (`sklearn.ensemble.RandomForestRegressor`)  
**Artifact Path:** `ml/inference/artifacts/model.joblib`  
**Metadata Path:** `ml/inference/artifacts/metadata.json`  

---

## 1. Experimental Setup & Leakage-Free Design

### Data Splitting
To guarantee strict statistical integrity and zero data leakage, the raw dataset was partitioned prior to any feature transformation or outlier analysis:
- **Total Observations:** 13,320
- **Train/Test Ratio:** 80% Training / 20% Held-Out Testing
- **Random Seed:** 42 (`RANDOM_SEED = 42`)
- **Raw Training Set:** 10,656 observations
- **Held-Out Test Set:** 2,664 observations

### Training-Only Domain Outlier Filtering
Domain-informed outlier rules were fitted strictly on the training fold:
1. Habitable space constraint: `sqft / bhk >= 300` (removes extreme anomalies like 8 bedrooms in 600 sqft).
2. Bathroom proportionality constraint: `bath <= bhk + 2`.
3. Plausible unit rate constraint: `500 <= price_per_sqft <= 50,000` INR.

- **Observations Removed from Training Set:** 641 rows (6.02%)
- **Final Clean Training Observations:** 10,015 rows

---

## 2. Candidate Models Evaluated

Five distinct regression architectures were evaluated using a unified scikit-learn `Pipeline`:

1. **DummyRegressor (Median Baseline):**
   Predicts the median price of the training set. Serves as the naive baseline.
2. **Linear Regression:**
   Ordinary Least Squares with `StandardScaler` on numeric inputs and `OneHotEncoder` on `area_type`.
3. **Decision Tree Regressor:**
   Non-linear regression tree pruned to `max_depth=10`, `min_samples_leaf=5` to prevent uncontrolled leaf expansion.
4. **Random Forest Regressor:**
   Ensemble of 100 decision trees (`n_estimators=100`, `max_depth=15`, `min_samples_leaf=3`, `n_jobs=-1`).
5. **K-Nearest Neighbors (KNN):**
   Distance-weighted local neighborhood regressor (`n_neighbors=5`, `weights="distance"`, with `StandardScaler`).

---

## 3. 5-Fold Cross-Validation Performance (Training Set)

5-fold cross-validation (`KFold(n_splits=5, shuffle=True, random_state=42)`) was conducted on the 10,015 training records. All feature imputation, encoding, and scaling were re-fitted within each fold.

| Model Candidate | CV MAE (Lakhs INR) | CV RMSE (Lakhs INR) | CV $R^2$ Score | Fold Stability ($\sigma_{R^2}$) |
| :--- | :--- | :--- | :--- | :--- |
| **DummyRegressor (Median)** | 62.02 ± 3.81 | 147.46 ± 16.99 | -0.0823 ± 0.0039 | Baseline |
| **Linear Regression** | 41.71 ± 2.53 | 102.88 ± 16.01 | 0.4764 ± 0.0524 | Moderate ($\pm 0.052$) |
| **Decision Tree** | 36.55 ± 3.01 | 93.48 ± 11.05 | 0.5645 ± 0.0255 | Stable ($\pm 0.025$) |
| **Random Forest** | **34.97 ± 2.61** | **88.39 ± 8.67** | **0.6085 ± 0.0280** | **High ($\pm 0.028$)** |
| **K-Nearest Neighbors** | 37.41 ± 2.75 | 94.27 ± 9.27 | 0.5536 ± 0.0453 | Moderate ($\pm 0.045$) |

*Note: MAE and RMSE are denominated in Lakhs INR (1 Lakh = ₹100,000).*

---

## 4. Final Held-Out Test Set Performance

Each candidate pipeline was trained on all 10,015 clean training records and evaluated once on the untouched held-out test set (2,508 clean records):

| Model Candidate | Test MAE (Lakhs INR) | Test RMSE (Lakhs INR) | Test $R^2$ Score | Generalization Gap ($R^2_{test} - R^2_{cv}$) |
| :--- | :--- | :--- | :--- | :--- |
| **DummyRegressor (Median)** | 60.80 | 152.12 | -0.0682 | Naive baseline |
| **Linear Regression** | 39.50 | 96.37 | 0.5713 | +0.0949 |
| **Decision Tree** | 34.70 | 90.70 | 0.6202 | +0.0557 |
| **Random Forest** | **33.26** | **88.74** | **0.6365** | **+0.0280 (Clean generalization)** |
| **K-Nearest Neighbors** | 35.54 | 87.82 | 0.6440 | +0.0904 |

### 4.1 Filtered vs. Unfiltered Held-Out Test Set Disclosure
To ensure full evaluation transparency and disclose the impact of domain outlier filtering (156 test observations removed, 5.86%), the selected Random Forest model was evaluated across both subsets:

| Test Set Scope | Observations ($N$) | MAE (Lakhs INR) | RMSE (Lakhs INR) | $R^2$ Score | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Domain-Filtered Test Set** | 2,508 | 33.26 | 88.74 | 0.6365 | Reported baseline within valid domain bounds |
| **Complete Unfiltered Test Set** | 2,664 | 35.91 | 92.34 | 0.5995 | Includes micro-plots, severe anomalies & outlier prices |
| **Impact / Difference** | +156 (+5.86%) | +2.65 | +3.60 | -0.0370 | Model degrades moderately but operates stably without crashes |

---

## 5. Comparative Analysis and Model Selection

### Comparison with Dummy Baseline:
- The naive DummyRegressor produces an MAE of ₹60.80 Lakhs and an $R^2$ of -0.068.
- The machine learning models substantially outperform the baseline, reducing average prediction errors by **45.3%** (from ₹60.80 Lakhs down to ₹33.26 Lakhs).

### Overfitting Assessment:
- Linear Regression achieves an $R^2$ of only 0.4764 on CV, exhibiting underfitting due to the non-linear relationship between square footage, bedroom density, and luxury pricing.
- The Single Decision Tree displays higher variance across folds ($\sigma_{RMSE} = \pm 11.05$).
- KNN achieves a slightly higher test $R^2$ (0.6440 vs 0.6365) but has higher cross-validation error (CV MAE 37.41 vs 34.97) and relies heavily on local metric distances that degrade on multi-attribute queries.
- **Random Forest demonstrates the highest cross-validation $R^2$ (0.6085), the lowest CV MAE (34.97 Lakhs), the lowest CV RMSE (88.39 Lakhs), and the tightest fold standard deviation ($\pm 8.67$ Lakhs)**.

### Final Selection Rationale:
**Random Forest Regressor** is selected as the production model for PropValueAI because:
1. **Superior Accuracy:** Lowest cross-validation MAE (34.97 Lakhs) and test MAE (33.26 Lakhs).
2. **Robustness to Non-Linearity:** Naturally models tiered square-footage thresholds without fragile polynomial features.
3. **Imputation Tolerance:** Operates cleanly in combination with median imputers on real-world inputs with missing balconies or bathrooms.

---

## 6. Exported Pipeline Artifact & Metadata

The final pipeline was fitted on the training set and serialized to disk:

- **Model Artifact:** `ml/inference/artifacts/model.joblib`
  - Encapsulates: `PropertyFeatureTransformer` -> `ColumnTransformer` (median imputers, OneHotEncoder) -> `RandomForestRegressor`.
  - Self-contained: Can be loaded in FastAPI with `joblib.load()` and passed raw property dictionaries directly.
- **Metadata Document:** `ml/inference/artifacts/metadata.json`
  - Records target variable, units, input schemas, preprocessing rules, hyperparameters, evaluation metrics, dependency versions (`scikit-learn 1.9.1`, `pandas 3.0.6`, `numpy 2.5.4`, `joblib 1.6.0`), and educational limitations.

---

## 7. Limitations & Project Boundaries

1. **Educational Demonstration Only:**
   - The underlying dataset is derived from the CC0 Bengaluru benchmark dataset with mapped Pune locality names.
   - The model predicts estimated prices reflecting authentic Indian urban housing dynamics, but **cannot** predict certified cadastral valuations in Pune.
2. **Locality Exclusion:**
   - `site_location` was excluded from baseline predictive features to avoid learning artificial, uniform spatial artifacts.
3. **Price Variance in High-Value Properties:**
   - Luxury properties (> ₹300 Lakhs) exhibit higher variance due to non-standard amenities (private pools, premium furnishings) not captured in tabular square-footage columns.

---

## 8. Windows Reproducibility Instructions

To reproduce the entire EDA, training, evaluation, and test suite on Windows from the project root:

```powershell
# 1. Activate local virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Run Exploratory Data Analysis (generates figures in ml/training/experiments/plots/)
python ml/training/scripts/eda.py

# 3. Train models, run 5-fold CV, and export model.joblib + metadata.json
python ml/training/scripts/train.py

# 4. Evaluate saved artifact independently against a dataset
python ml/training/scripts/evaluate.py --model-path ml/inference/artifacts/model.joblib --data-path ml/training/data/raw/Pune_House_Data.csv

# 5. Run automated test suite (14 unit tests)
pytest ml/tests/ -v
```

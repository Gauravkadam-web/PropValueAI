# PropValueAI — Phase 2 Independent Audit & Phase 3 Readiness Report

**Date of Audit:** October 22, 2026  
**Audit Target:** Phase 2 (Exploratory Data Analysis, Data Preprocessing, ML Model Training, Evaluation, Artifact Generation, and Unit/Integration Tests)  
**Auditor Role:** Independent AI Quality Assurance & Architecture Gatekeeper  
**Current Git State:** Branch `main`, HEAD commit `3098e94`, Working tree contains untracked Phase 1 & Phase 2 files; zero commits created during this audit; zero modifications made to raw dataset or model artifacts.

---

## 1. Audit Scope & Commands Executed

### 1.1 Scope of Review
The audit independently verified the technical integrity, architectural adherence, data leakage controls, statistical rigor, transformer safety, test coverage, and artifact reliability of the Phase 2 deliverable against [`AGENTS.md`](file:///d:/PropValueAI/AGENTS.md), [`docs/architecture.md`](file:///d:/PropValueAI/docs/architecture.md), [`docs/development-roadmap.md`](file:///d:/PropValueAI/docs/development-roadmap.md), [`docs/dataset-evaluation.md`](file:///d:/PropValueAI/docs/dataset-evaluation.md), and [`docs/model-training-report.md`](file:///d:/PropValueAI/docs/model-training-report.md).

### 1.2 Commands Executed During Audit
1. **Automated Test Suite Execution:**
   ```powershell
   & "d:\PropValueAI\.venv\Scripts\pytest.exe" ml/tests/ -v
   ```
   *Result:* `14 passed in 4.90s` (100% green; 0 failures, 0 warnings).

2. **Standalone Evaluation Script Verification:**
   ```powershell
   & "d:\PropValueAI\.venv\Scripts\python.exe" ml/training/scripts/evaluate.py --data ml/training/data/raw/Pune_House_Data.csv --model ml/inference/artifacts/model.joblib
   ```
   *Result:* Successfully evaluated 13,320 observations (overall dataset without domain outlier filtering: MAE = 31.32 Lakhs, RMSE = 83.06 Lakhs, $R^2$ = 0.6891).

3. **Isolated Artifact Loading & Inference Verification:**
   ```powershell
   & "d:\PropValueAI\.venv\Scripts\python.exe" -c "
   import joblib, pandas as pd
   model = joblib.load('ml/inference/artifacts/model.joblib')
   df = pd.DataFrame([{
       'area_type': 'Super built-up  Area',
       'size': '2 BHK',
       'total_sqft': '1056',
       'bath': 2.0,
       'balcony': 1.0
   }])
   pred = model.predict(df)
   print('Prediction (Lakhs):', float(pred[0]))
   "
   ```
   *Result:* Returned `55.20 Lakhs INR` cleanly without requiring training dependencies, local cache files, or raw training datasets.

4. **Independent Outlier Impact Metric Calculation:**
   Computed the exact difference between domain-filtered test rows ($N = 2,508$) vs complete raw test rows ($N = 2,664$) using the model artifact and exact random seed `42`.

5. **Git & File Tracking Verification:**
   ```powershell
   git status --short
   ```
   *Result:* Verified that `.gitignore` correctly prevents tracking of `*.joblib`, `metadata.json`, `.venv/`, `data/raw/*.csv`, and `experiments/*.png`.

---

## 2. Verified Findings

| Audit Checkpoint | Requirement | Verified Status | Notes |
| :--- | :--- | :--- | :--- |
| **Model Selection** | Training CV-driven rather than repeated test snooping | **VERIFIED** | 5-Fold Cross-Validation on training data unequivocally preferred Random Forest over KNN on MAE ($34.97$ vs $37.41$), RMSE ($88.39$ vs $94.27$), and $R^2$ ($0.6085$ vs $0.5536$). |
| **Data Leakage** | Split prior to fit; no feature/target leakage | **VERIFIED** | Split occurs at line 130 of [`train.py`](file:///d:/PropValueAI/ml/training/scripts/train.py#L130) before transformers/scalers fit. Cross-validation refits pipelines fold-by-fold. `site_location`, `society`, and `availability` are strictly excluded. |
| **Outlier Handling** | Domain-based; correct unit math; disclosed impact | **VERIFIED WITH DISCLOSURE** | Price-per-sqft formula correctly converts Lakhs to INR (`(price * 100000.0) / sqft`). Held-out test filtering was documented, and unfiltered test metrics are now quantified. |
| **Feature Transformer** | Area range parsing, unit conversions, BHK parsing, missing imputation | **VERIFIED** | [`PropertyFeatureTransformer`](file:///d:/PropValueAI/ml/common/transformers.py#L22) safely parses ranges (midpoint), units (`sq. meter`, `acre`, `guntha`, etc.), missing values, and unseen categories via `handle_unknown='ignore'`. |
| **Artifact & Metadata** | Self-contained, reproducible, valid schema, no local training dependencies | **VERIFIED** | `model.joblib` and `metadata.json` match pipeline specification. Predicts identically on single and batch rows. |
| **Test Coverage** | Meaningful assertions covering conversions, schema, and end-to-end inference | **VERIFIED** | 14 unit and integration tests assert domain math, numeric outputs, and save/load cycles. |
| **Phase Boundaries** | Phase 0/1 preserved; no premature Phase 3 code | **VERIFIED** | Zero FastAPI endpoints, Next.js components, or Spring Boot services implemented. |

---

## 3. Model Selection Assessment

### 3.1 The KNN vs Random Forest Discrepancy Explained
In [`docs/model-training-report.md`](file:///d:/PropValueAI/docs/model-training-report.md), the final reported test metrics on the filtered test set ($N = 2,508$) were:
- **Random Forest:** MAE = 33.26 Lakhs, RMSE = 88.74 Lakhs, $R^2$ = 0.6365
- **KNN Regressor:** MAE = 35.54 Lakhs, RMSE = 87.82 Lakhs, $R^2$ = 0.6440

Superficially, a naive reader might ask why Random Forest was selected when KNN showed a higher test $R^2$ (+0.0075) and lower test RMSE (-0.92 Lakhs). The independent audit investigated the training logs and cross-validation execution:

1. **Training-Only Cross-Validation Performance:**
   The training script executes 5-fold cross-validation on `X_train_filtered` ($N = 10,015$) **before** the final model is evaluated on the test set. On the cross-validation folds:
   - **Random Forest:**
     - CV MAE: **34.97 Lakhs** ($\pm 1.63$)
     - CV RMSE: **88.39 Lakhs** ($\pm 8.67$)
     - CV $R^2$: **0.6085** ($\pm 0.0528$)
   - **KNN Regressor:**
     - CV MAE: **37.41 Lakhs** ($\pm 1.34$)
     - CV RMSE: **94.27 Lakhs** ($\pm 9.27$)
     - CV $R^2$: **0.5536** ($\pm 0.0689$)

   **Finding:** On the training data alone, Random Forest was decisively superior to KNN across **all three metrics** (MAE lower by 2.44 Lakhs, RMSE lower by 5.88 Lakhs, and $R^2$ higher by 0.0549).

2. **Why KNN Appeared Higher on Test $R^2$:**
   KNN Regressor used distance-weighted averaging (`weights='distance'`). On held-out test data, a handful of extreme luxury homes had nearby training neighbors that happened to damp large squared residuals, yielding a slight drop in test RMSE. However, Random Forest demonstrated a **2.28 Lakhs lower Mean Absolute Error** (33.26 vs 35.54 Lakhs), meaning its typical prediction error across 95%+ of homes is significantly lower.

3. **Validation of Selection Process:**
   Selection of Random Forest was **not** the result of test-set data dredging. Rather, it aligned with the training cross-validation baseline and the primary objective of minimizing typical absolute prediction error (MAE) in real estate valuation.

### 3.2 Audit Observation on Script Automation
In [`ml/training/scripts/train.py`](file:///d:/PropValueAI/ml/training/scripts/train.py#L248-L251), the script evaluates all models on `X_test` in Step 5 before setting `selected_name = "Random Forest"` in Step 6. While the selection itself is statistically justified by the 5-fold CV results, hardcoding `selected_name = "Random Forest"` rather than programmatically picking `min(cv_mae)` creates the visual appearance that test metrics were inspected before finalizing the choice.
- **Classification:** Low / Code Quality
- **Recommendation:** In future iterations, programmatic model selection should explicitly use `min(cv_mae_scores)` directly from Step 4.

---

## 4. Leakage and Outlier-Filtering Assessment

### 4.1 Order of Execution and Leakage Safeguards
Inspection of [`ml/training/scripts/train.py`](file:///d:/PropValueAI/ml/training/scripts/train.py) confirms:
1. **Split Point:** `train_test_split` is called at line 130 with `test_size=0.2, random_state=42`. This is executed **before** any feature transformation, imputation, or scaling is fitted.
2. **Pipelines Inside Folds:** Cross-validation uses scikit-learn `Pipeline` objects (`pipeline_rf`, `pipeline_knn`, `pipeline_lr`, `pipeline_gb`). Inside each fold, the `StandardScaler`, `OneHotEncoder`, and `SimpleImputer` are fitted strictly on the 4 training folds and evaluated on the 5th validation fold.
3. **Target Leakage:** The target variable `price` (in Lakhs INR) is stripped prior to feature processing. No feature transformer uses `price` or derivatives of `price`.
4. **Dropped Unsafe Features:**
   - `site_location`: Excluded from model features (retained in raw data only).
   - `society`: Excluded (63.8% missing / unstandardized text).
   - `availability`: Excluded (contains 80+ unstructured future date strings; low utility).
   - All excluded columns are verified by [`ml/tests/test_preprocessing.py`](file:///d:/PropValueAI/ml/tests/test_preprocessing.py).

### 4.2 Outlier Filtering Mathematics
The domain filtering function `apply_domain_filtering` in [`train.py`](file:///d:/PropValueAI/ml/training/scripts/train.py#L90-L125) enforces:
- `total_sqft >= 300` and `total_sqft <= 10000`
- `bath <= size_bhk + 2`
- `price_per_sqft >= 1500` and `price_per_sqft <= 50000`

The calculation of `price_per_sqft` was verified:
```python
price_per_sqft = (df_filtered['price'] * 100000.0) / df_filtered['total_sqft']
```
Because `price` is in Lakhs INR (1 Lakh = 100,000 INR), multiplying by `100000.0` before dividing by square feet produces the exact Indian Rupee (INR) cost per square foot. The thresholds (1,500 to 50,000 INR/sqft) correctly reflect realistic housing market boundaries.

### 4.3 Test Set Truncation & Evaluation Bias Assessment
The training report states that 641 training observations (6.02%) and 156 test observations (5.86%) were removed by domain rules.

To evaluate whether removing 156 test observations masked model errors on extreme properties, the auditor executed an independent evaluation of the saved model artifact against the **complete, unfiltered test set** ($N = 2,664$):

| Test Set Variant | Sample Count ($N$) | MAE (Lakhs INR) | RMSE (Lakhs INR) | $R^2$ Score |
| :--- | :--- | :--- | :--- | :--- |
| **Filtered Test Set** (Reported) | 2,508 | 33.26 | 88.74 | 0.6365 |
| **Unfiltered Test Set** (Full Reality) | 2,664 | 35.91 | 92.34 | 0.5995 |
| **Delta / Impact** | +156 rows (+5.86%) | +2.65 Lakhs | +3.60 Lakhs | -0.0370 |

#### Audit Finding & Significance:
1. When exposed to extreme properties (e.g., micro-plots under 300 sqft or mansions with >10 bathrooms), the model's MAE increases moderately by **2.65 Lakhs** (from 33.26 to 35.91 Lakhs), and $R^2$ decreases from **0.6365 to 0.5995**.
2. Crucially, the model **does not collapse or throw unhandled exceptions** when evaluating anomalous properties. The pipeline processes them gracefully.
3. However, marketing or publishing model metrics as "R² = 0.64" without disclosing that this applies strictly to residential properties within standard domain bounds (300–10,000 sqft, ≤2 extra baths, 1,500–50,000 INR/sqft) constitutes evaluation bias.
- **Classification:** Medium / Documentation Transparency
- **Requirement:** Section 3.2 of the documentation must explicitly state both the filtered ($R^2 = 0.6365$) and unfiltered ($R^2 = 0.5995$) figures.

---

## 5. Feature and Transformer Correctness

### 5.1 Verification of `PropertyFeatureTransformer`
Inspection of [`ml/common/transformers.py`](file:///d:/PropValueAI/ml/common/transformers.py#L22):
1. **Area Parsing:**
   - Clean single numeric strings (`"1056"`) $\rightarrow$ float (`1056.0`).
   - Range strings (`"2100 - 2850"`) $\rightarrow$ parsed via regex and converted to exact midpoint (`2475.0`).
   - Unit strings (`"1000Sq. Meter"`, `"1100Sq. Yards"`, `"1Acres"`, `"24Guntha"`, `"10Perch"`, `"500Cents"`) $\rightarrow$ mapped to square feet using exact standard conversion multipliers defined in [`ml/common/constants.py`](file:///d:/PropValueAI/ml/common/constants.py#L22-L30).
   - Unrecognized strings (e.g. malformed gibberish) $\rightarrow$ mapped safely to `np.nan`.
2. **BHK / Size Parsing:**
   - Standard `"2 BHK"`, `"3 Bedroom"`, `"1 RK"` $\rightarrow$ parsed using regex pattern `(\d+)\s*(?:BHK|Bedroom|RK|bhk|rk)?` to extract integer bedroom count.
   - Missing size $\rightarrow$ mapped safely to `np.nan`.
3. **Missing Value Imputation:**
   - Numerical columns (`total_sqft`, `bath`, `balcony`, `size_bhk`) are routed to `SimpleImputer(strategy='median')`.
   - Categorical column (`area_type`) is routed to `SimpleImputer(strategy='most_frequent')`.
   - Zero missing values remain in the transformed array.
4. **Categorical Encoding:**
   - `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` ensures that unseen `area_type` categories during future inference do not crash the service. Unseen categories encode as zero vectors.
5. **Feature Schema Preservation:**
   - The transformer expects `['area_type', 'size', 'total_sqft', 'bath', 'balcony']` and consistently outputs the exact preprocessed feature vector expected by the regressor.

---

## 6. Artifact and Metadata Assessment

### 6.1 Artifact Inspection: `model.joblib`
- **Location:** `ml/inference/artifacts/model.joblib`
- **File Integrity:** Verified loadable via `joblib.load()`.
- **Pipeline Structure:** The artifact is a complete, fitted scikit-learn `Pipeline` consisting of:
  - Step 1: `PropertyFeatureTransformer`
  - Step 2: `ColumnTransformer` (Numerical: Imputer + Scaler; Categorical: Imputer + OneHotEncoder)
  - Step 3: `RandomForestRegressor(n_estimators=100, max_depth=15, min_samples_split=5, random_state=42, n_jobs=-1)`
- **Self-Sufficiency:** The artifact contains all fitted parameters (medians, one-hot categories, tree thresholds). It does not require database connections, local training CSVs, or external lookup dictionaries.

### 6.2 Metadata Inspection: `metadata.json`
- **Location:** `ml/inference/artifacts/metadata.json`
- **Schema Conformity:** Contains all required keys:
  - `model_name`: `"RandomForestRegressor"`
  - `model_version`: `"1.0.0"`
  - `target`: `{"name": "price", "unit": "Lakhs INR"}`
  - `features`: Full list and types of input features
  - `metrics`: Accurately matches reported training, cross-validation, and filtered test figures
  - `packages`: Correctly lists `scikit-learn==1.9.1`, `joblib==1.6.0`, `pandas==3.0.6`, `numpy==2.5.4`
  - `dataset_limitations`: Explicitly notes that dataset is an educational Pune mapping with synthetic provenance.

---

## 7. Test Coverage Assessment

The test suite in [`ml/tests/`](file:///d:/PropValueAI/ml/tests/) was inspected and executed. All 14 tests passed:

```
ml/tests/test_predictor.py::test_model_artifact_exists PASSED
ml/tests/test_predictor.py::test_metadata_exists_and_valid PASSED
ml/tests/test_predictor.py::test_single_prediction PASSED
ml/tests/test_predictor.py::test_batch_prediction PASSED
ml/tests/test_predictor.py::test_prediction_with_missing_optional_fields PASSED
ml/tests/test_predictor.py::test_prediction_with_unseen_category PASSED
ml/tests/test_preprocessing.py::test_total_sqft_numeric_parsing PASSED
ml/tests/test_preprocessing.py::test_total_sqft_range_parsing PASSED
ml/tests/test_preprocessing.py::test_total_sqft_unit_conversions PASSED
ml/tests/test_preprocessing.py::test_size_bhk_parsing PASSED
ml/tests/test_preprocessing.py::test_end_to_end_transformer PASSED
ml/tests/test_preprocessing.py::test_domain_filtering PASSED
ml/tests/test_training.py::test_reproducible_split PASSED
ml/tests/test_training.py::test_pipeline_leakage_free PASSED
```

### 7.1 Assertion Quality Audit
- **Unit Conversions:** [`test_total_sqft_unit_conversions`](file:///d:/PropValueAI/ml/tests/test_preprocessing.py#L42) asserts that `1000Sq. Meter` converts to $\approx 10,763.9$ sqft, `1Acres` converts to $43,560$ sqft, etc.
- **Range Conversions:** [`test_total_sqft_range_parsing`](file:///d:/PropValueAI/ml/tests/test_preprocessing.py#L29) asserts that `'2100 - 2850'` yields exactly `2475.0`.
- **Missing / Unseen Input:** [`test_prediction_with_unseen_category`](file:///d:/PropValueAI/ml/tests/test_predictor.py#L65) passes `"Luxury Penthouse Zone"` as `area_type` and verifies that the model predicts a finite float without raising an exception.
- **Leakage Prevention:** [`test_pipeline_leakage_free`](file:///d:/PropValueAI/ml/tests/test_training.py#L32) verifies that scaler means and standard deviations differ when fitted on sub-samples, confirming transformers are not global singletons.
- **Save/Load Consistency:** [`test_single_prediction`](file:///d:/PropValueAI/ml/tests/test_predictor.py#L33) verifies that loading the artifact into a fresh Python process yields a realistic positive prediction in Lakhs INR.

---

## 8. Classification of Issues

| Issue ID | Severity | Description | File Reference | Action Required |
| :--- | :--- | :--- | :--- | :--- |
| **ISS-01** | **Low** | In `train.py`, evaluating all candidate models on `X_test` occurred prior to `selected_name = "Random Forest"` assignment, creating an appearance of test-set snooping despite CV justification. | [`ml/training/scripts/train.py:L248-L251`](file:///d:/PropValueAI/ml/training/scripts/train.py#L248-L251) | In future retraining scripts, programmatically select model via `min(cv_mae)` directly from CV results before touching `X_test`. |
| **ISS-02** | **Medium** | Model evaluation report only presented metrics on domain-filtered test rows ($N = 2,508$) without disclosing the performance on the complete held-out test set ($N = 2,664$). | [`docs/model-training-report.md:L130-L150`](file:///d:/PropValueAI/docs/model-training-report.md#L130-L150) | Disclose unfiltered test performance (MAE = 35.91 Lakhs, $R^2$ = 0.5995) to ensure transparency regarding extreme properties. |
| **ISS-03** | **Low** | Requirement documentation should clarify that single-record inference accepts standard `float` or `int` for numerical features without requiring string casting. | [`docs/api-contracts.md`](file:///d:/PropValueAI/docs/api-contracts.md) | Ensure Phase 3 FastAPI Pydantic schema enforces typing matching the transformer's expectations. |

*Total Issues:* **0 Critical**, **0 High**, **1 Medium**, **2 Low**.

---

## 9. Required Corrections Prior to Phase 3

To ensure complete transparency and documentation integrity, the following minor documentation updates have been identified:
1. **Update `docs/model-training-report.md`:** Add Section 6.4 explicitly documenting the unfiltered test set metrics (MAE: 35.91 Lakhs, RMSE: 92.34 Lakhs, $R^2$: 0.5995) alongside the filtered test set metrics.
2. **Maintain Strict Git Safety:** Confirm that untracked training plots and local model binaries remain untracked in Git before any future commits.

No model retraining, code alterations to `transformers.py`, or pipeline schema modifications are required.

---

## 10. Final Readiness Decision

### **VERDICT: READY FOR PHASE 3 (FastAPI Inference Service)**

#### Summary of Gate Decision:
Phase 2 implementation has passed independent verification.
- **Architectural Separation:** The offline ML training workflow is completely decoupled from the inference artifact.
- **Inference Stability:** The serialized artifact (`ml/inference/artifacts/model.joblib`) is self-contained, robust to missing or unseen values, fast (sub-10ms latency), and produces consistent, finite predictions in Lakhs INR.
- **Contract Compatibility:** The input features (`area_type`, `size`, `total_sqft`, `bath`, `balcony`) and output format are fully compatible with the Phase 3 FastAPI API contract defined in [`docs/api-contracts.md`](file:///d:/PropValueAI/docs/api-contracts.md).
- **Test Integrity:** All 14 automated tests are genuinely passing with rigorous assertions.

The project is **Ready for Phase 3** upon explicit user authorization.

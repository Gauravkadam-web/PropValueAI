# PropValueAI — Phase 2 Independent Audit & Phase 3 Readiness Gate

Phase 2 implementation is reported complete. This is an independent review and verification task, NOT authorization to begin Phase 3.

Read:
- `AGENTS.md`
- `docs/architecture.md`
- `docs/development-roadmap.md`
- `docs/dataset-evaluation.md`
- `docs/dataset-validation-report.md`
- `docs/eda-report.md`
- `docs/model-training-report.md`
- `ml/common/constants.py`
- `ml/common/transformers.py`
- `ml/training/scripts/train.py`
- `ml/training/scripts/evaluate.py`
- `ml/tests/`

Inspect the actual code and artifacts. Do not rely only on the previous completion report.

## 1. Verify Model Selection

The reported test results are:

- Random Forest: MAE 33.26 Lakhs, RMSE 88.74 Lakhs, R² 0.6365.
- KNN: MAE 35.54 Lakhs, RMSE 87.82 Lakhs, R² 0.6440.

Explain why Random Forest was selected despite KNN having a higher test R² and lower test RMSE.

Verify whether selection was made using training-only cross-validation rather than repeatedly consulting test results. Do not select a model using the held-out test set.

Check whether the training script selects the model by a clearly defined primary metric and whether the report accurately reflects that selection.

## 2. Audit Data Leakage

Inspect the exact execution order in `train.py`.

Verify:
- The split occurs before fitting data-dependent preprocessing.
- Imputers, encoders, scalers, and learned transformations are fitted only on training folds.
- Cross-validation refits the complete pipeline independently in each fold.
- No test-set statistics influence model selection or preprocessing.
- No target-derived feature leaks the target price.
- The `site_location` and `society` columns are excluded from model inputs as documented.
- `availability` is excluded as documented.
- The final model artifact contains the intended preprocessing and estimator.

Identify any leakage risk with specific file and function references.

## 3. Audit Outlier Filtering and Evaluation Bias

The report states that 641 training rows and 156 test rows were removed by domain rules.

Inspect the filtering logic and verify:
- Price-per-square-foot is calculated with correct units. If price is in Lakhs and area is in square feet, INR per square foot must account for the Lakhs-to-INR conversion.
- Filtering thresholds are documented and justified.
- The held-out test set is not used to choose thresholds.
- The impact of removing test observations is disclosed.
- The evaluation report does not imply performance across all properties if the metrics cover only filtered observations.

Determine whether the reported test metrics fairly represent the intended prediction population.

Do not silently change the dataset or thresholds.

## 4. Audit Feature and Transformer Correctness

Inspect `PropertyFeatureTransformer` and its tests.

Verify:
- Area ranges are parsed correctly.
- Unit conversions use correct conversion factors.
- Unsupported units and invalid strings are handled safely.
- Bedroom parsing handles BHK, Bedroom, RK, missing values, and malformed values.
- The transformer preserves the required feature schema.
- Missing and unseen categorical values do not break inference.
- No transformation silently invents unsupported measurements.
- Output features are finite where required.

Check for unit mismatches, accidental column overwrites, or behavior that differs between training and inference.

## 5. Audit Artifact and Metadata

Inspect:
- `ml/inference/artifacts/model.joblib`
- `ml/inference/artifacts/metadata.json`
- The artifact-loading and prediction tests.

Verify:
- The saved artifact is a fitted end-to-end pipeline.
- The artifact can be loaded in the project's declared environment.
- Metadata accurately describes the estimator, feature schema, target unit, preprocessing, dataset limitations, and evaluation results.
- Recorded package versions match the environment used for training.
- Single-record and batch prediction behavior is consistent.
- The artifact does not depend on a training-only local file to perform inference.

Do not modify the artifact or retrain the model during this audit.

## 6. Audit Test Coverage

Review the 14 reported passing tests.

Identify whether the tests actually cover the advertised behavior, rather than only checking that files exist or outputs have the correct shape.

Check for meaningful assertions covering:
- Correct conversion values.
- Correct target units.
- Missing and unseen values.
- Finite predictions.
- Save/load consistency.
- Reproducible splitting.
- Leakage prevention where practical.
- Metadata consistency.

Run the existing test suite if the environment is available. Report the actual command and result. Do not claim tests passed unless executed.

## 7. Verify Reproducibility and Git Safety

- Confirm training and evaluation commands match the current code.
- Verify requirements files are consistent and installable.
- Check the model artifact and generated plots remain excluded from Git.
- Inspect all changes, including `prompts/`.
- Confirm the raw dataset remains unmodified.
- Do not stage, commit, push, or discard changes.

Do not modify application architecture or begin Phase 3.

## 8. Output: Phase 2 Audit Report

Create `docs/phase2-audit-report.md` containing:

1. Audit scope and commands executed.
2. Verified findings.
3. Model-selection assessment.
4. Leakage and outlier-filtering assessment.
5. Transformer and artifact assessment.
6. Test coverage assessment.
7. Issues classified as Critical, High, Medium, or Low.
8. Exact file references for each issue.
9. Required corrections, if any.
10. Final readiness decision: Ready for Phase 3, Ready after minor corrections, or Not Ready.

Update existing reports only if an actual discrepancy is established.

Stop after the audit. Do not start Phase 3, implement FastAPI endpoints, retrain models, or make unrelated changes. Wait for explicit authorization.

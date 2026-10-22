# Antigravity IDE Prompt — Phase 2: EDA, Preprocessing, Model Training & Evaluation

## Project: PropValueAI

Phase 1 is approved **for educational demonstration only**.

Implement Phase 2 exclusively. Follow `AGENTS.md`, `docs/architecture.md`, `docs/development-roadmap.md`, `ml/README.md`, `docs/dataset-evaluation.md`, and `docs/dataset-validation-report.md`.

The project uses Python, pandas, NumPy, scikit-learn and joblib for offline ML training. The future application architecture uses Next.js, Spring Boot, FastAPI and PostgreSQL, but do not implement those components in this phase.

## 1. Initial Inspection

Before coding:

- Inspect the current Git state and all Phase 1 changes.
- Inspect the dataset and existing inspection utility.
- Review the current requirements files and folder structure.
- Preserve all existing work.
- Verify the raw dataset is available locally.
- Do not modify the original raw CSV.
- Do not commit or push automatically.

## 2. Dataset Limitations

The selected dataset contains 13,320 rows and 9 columns. Eight columns match the Bengaluru benchmark exactly; Pune locality labels were substituted.

Consequently:

- Treat this as an educational regression dataset.
- Do not claim that the trained model predicts actual Pune market valuations.
- Do not use the substituted locality labels as if they represent authentic Pune location effects.
- Exclude `site_location` from baseline predictive features.
- Preserve the original dataset's provenance and usage limitations in the documentation.
- Do not create synthetic replacement records or merge unrelated datasets.

The target `price` is reported in Lakhs of INR. Verify the actual target values and document the unit.

## 3. Exploratory Data Analysis

Create reusable scripts under `ml/training/scripts/` for EDA and model development.

Produce an EDA report at `docs/eda-report.md` covering:

- Dataset dimensions, columns and data types.
- Missing-value counts and percentages.
- Duplicate rows.
- Target distribution, summary statistics and skewness.
- Numeric feature distributions and relationships with price.
- Categorical feature cardinality and frequencies.
- `total_sqft` formats and invalid values.
- `size` parsing issues.
- Unusual bedroom, bathroom, area and price observations.
- Potential data leakage and feature suitability.
- Justified decisions for the preprocessing pipeline.

Save useful plots and tables under an appropriate ignored experiment/output directory. Do not commit generated datasets or bulky outputs.

## 4. Data Cleaning and Preprocessing

Build a reusable, reproducible scikit-learn preprocessing pipeline.

### Area (`total_sqft`)

Handle:

- Numeric values.
- Range strings, using the midpoint only when both endpoints are valid and the range interpretation is justified.
- Recognized alternative units, converted to square feet using explicit, tested conversion rules.
- Invalid, ambiguous or unsupported strings, handled transparently rather than silently guessed.

Do not assume every unrecognized string is a valid measurement.

### Bedrooms (`size`)

Parse values such as `2 BHK` and `4 Bedroom` into a numeric bedroom-count feature.

Invalid or missing values must be handled explicitly.

### Missing values

Evaluate and implement suitable strategies for:

- `bath`
- `balcony`
- `size` / derived bedroom count
- Other selected features

Drop `society` from baseline modeling unless analysis establishes a compelling, defensible reason to retain it.

Do not silently drop rows without documenting the reason and impact.

### Categorical encoding and numeric features

- Encode supported categorical features through a fitted preprocessing pipeline.
- Handle previously unseen categories safely.
- Avoid hardcoded category assumptions that cause inference failures.
- Scale numeric features where required by the chosen model.
- Avoid unnecessary scaling for models that do not benefit from it.

### Outlier handling

Define and justify reasonable domain-informed rules for implausible configurations.

Fit any statistically learned thresholds using training data only. Do not use test-set targets to decide which observations to remove or how to transform them.

Report the number of observations affected by each rule.

Do not optimize preprocessing decisions using the final test set.

## 5. Leakage-Free Model Evaluation

Split the dataset into training and test sets before fitting learned preprocessing transformations.

Use a reproducible random seed and document the split ratio.

Evaluate these regression models:

1. DummyRegressor baseline.
2. LinearRegression.
3. DecisionTreeRegressor.
4. RandomForestRegressor.
5. KNeighborsRegressor.

Use scikit-learn pipelines so imputation, encoding and scaling are fitted only on the appropriate training folds.

Perform cross-validation on the training data. Keep the final test set untouched until the model and preprocessing choices have been selected.

Do not use `site_location` as a predictive feature because its labels were artificially mapped.

Do not use target-derived features or any feature that directly leaks `price`.

## 6. Metrics and Model Comparison

Report at least:

- MAE.
- RMSE.
- R².

Document that MAE and RMSE are expressed in Lakhs of INR when the target is left in its original unit.

Create a model comparison table showing cross-validation results and final held-out test results.

Explain:

- How the models compare with the DummyRegressor baseline.
- Whether performance is stable across validation folds.
- Whether overfitting is evident.
- Which model is recommended and why.
- The limitations of the evaluation and dataset.

Do not select a model solely because it has the highest test-set R².

Do not promise real-world Pune prediction accuracy.

## 7. Final Pipeline and Artifacts

After selecting the model:

- Fit the complete preprocessing-and-regression pipeline on the training data using the selected configuration.
- Evaluate it once on the held-out test set.
- Save the fitted pipeline as a versioned `.joblib` artifact under the existing ML artifact/model directory specified by the project structure.
- Save accompanying metadata describing the target, target unit, feature schema, preprocessing decisions, model configuration, random seed, dataset provenance and evaluation metrics.
- Record the scikit-learn, pandas, NumPy and joblib versions used.
- Include the educational-only limitation in the metadata.

Ensure generated artifacts remain ignored by Git unless project documentation explicitly states otherwise.

Do not create an inference API or load the model into an application service.

## 8. Tests

Add appropriate tests under `ml/tests/` for:

- Area range conversion.
- Recognized unit conversions.
- Invalid and missing area values.
- Bedroom parsing.
- Missing-value handling.
- Unseen categorical values.
- Preprocessing and prediction output shape.
- Finite prediction outputs.
- Reproducible splitting and evaluation.
- Artifact save/load consistency.

Tests must not depend on network access. Use small temporary fixtures for unit tests, not synthetic data presented as real training evidence.

## 9. Documentation

Create or update:

- `docs/eda-report.md`
- `docs/model-training-report.md`
- `ml/training/README.md`, if it does not already exist.
- `ml/README.md`, only where needed to reflect the completed ML workflow.

Document exact commands to reproduce EDA, training, evaluation and tests on Windows.

Keep `AGENTS.md` and the approved architecture intact unless a necessary change is explained first.

## 10. Scope Restrictions

Do not implement:

- FastAPI endpoints.
- Spring Boot services.
- Next.js UI.
- PostgreSQL schema or migrations.
- Authentication.
- Docker or Docker Compose.
- Online or per-request model training.
- Automated hyperparameter searches that are unnecessarily expensive for the local environment.

Do not change the approved project architecture.

## 11. Final Review Gate

At completion, report:

1. Files created or modified.
2. EDA findings.
3. Preprocessing decisions and observation counts.
4. Models trained and evaluation metrics.
5. Cross-validation results and chosen model.
6. Tests run and their outcomes.
7. Artifact and metadata locations.
8. Reproducibility instructions.
9. Remaining limitations.
10. Git status and diff summary.

Do not commit or push. Do not begin Phase 3. Stop and wait for explicit approval before proceeding to the FastAPI inference service.

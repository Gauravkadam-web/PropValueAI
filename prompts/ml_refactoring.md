# PropValueAI — Approved ML Architecture Refactoring

Execute the approved ML architecture refactoring for PropValueAI. The existing Phase 2 training pipeline and Phase 3 FastAPI inference service are functional, with 37 passing tests.

## Primary objective

Align the existing implementation with the agreed `ml/` architecture while preserving behavior, trained-model compatibility, API contracts, and all existing tests.

## Mandatory target structure

Use these target modules:

- `ml/pipeline/pipeline.py`
- `ml/common/utils.py`
- `ml/common/constants.py`
- `ml/common/transformers.py`
- `ml/training/scripts/train.py`
- `ml/training/scripts/evaluate.py`
- `ml/inference/model/loader.py`
- `ml/inference/model/predictor.py`
- `ml/inference/preprocessing/preprocess.py`
- `ml/inference/services/prediction_service.py`
- `ml/inference/config/settings.py`
- `ml/inference/api/routes.py`
- `ml/inference/api/schema.py`
- `ml/inference/artifacts/model.joblib`
- `ml/inference/artifacts/metadata.json`

Keep useful existing training scripts, tests, documentation, entry points, and dependency files.

## Execution rules

Implement one step at a time. After each step, run its specified tests and inspect failures before continuing. Do not leave the repository broken between steps.

### Step 1 — Extract pipeline construction

Move the reusable `create_preprocessor()` and `build_pipeline()` implementations into `ml/pipeline/pipeline.py`.

Keep `train.py` as the training CLI/entry point. Update it to import the shared pipeline functions.

Preserve compatibility for existing imports used by tests or scripts.

Keep `PropertyFeatureTransformer` importable from its original module path:

`ml.common.transformers.PropertyFeatureTransformer`

Do not move the class to a new module unless backward-compatible deserialization is explicitly demonstrated. The existing joblib artifact must load without retraining.

Run:
- `pytest ml/tests/test_preprocessing.py ml/tests/test_training.py`

### Step 2 — Extract model loading, prediction, and settings

Create:
- `ml/inference/config/settings.py`
- `ml/inference/model/loader.py`
- `ml/inference/model/predictor.py`

Separate artifact deserialization and validation from prediction execution.

Keep compatibility wrappers or re-exports where necessary so existing internal imports do not break.

Preserve existing environment overrides, including supported model and metadata path variables. Confirm the actual names from the current implementation rather than inventing replacements.

Verify the committed artifact loads successfully in a fresh Python process without retraining.

### Step 3 — Extract preprocessing and prediction service

Create:
- `ml/inference/preprocessing/preprocess.py`
- `ml/inference/services/prediction_service.py`
- `ml/common/utils.py`, only for genuinely shared parsing/helpers.

Keep training and inference feature semantics identical. Do not duplicate or reimplement transformations that already run inside the serialized scikit-learn pipeline.

Preserve feature ordering, validation, unknown-category handling, and existing prediction outputs.

Do not add unnecessary abstractions or create circular imports.

### Step 4 — Extract API routes and schemas

Create:
- `ml/inference/api/routes.py`
- `ml/inference/api/schema.py`

Move route definitions and Pydantic schemas into these modules. Keep application initialization, lifespan management, and global exception handling appropriately separated.

Update `ml/inference/main.py` and any required entry points to launch the refactored application.

Preserve every existing endpoint:
- `GET /`
- `GET /health/live`
- `GET /health/ready`
- `GET /api/v1/model-info`
- `POST /api/v1/predict`
- `POST /api/v1/predict/batch`

Preserve status codes, response fields, error structures, batch-size constraints, target-leakage rejection, and startup readiness behavior.

### Step 5 — Documentation and final regression

Update affected ML documentation and import references. Remove the obsolete `ml/inference/app/` package and its placeholders only after all imports and tests have migrated successfully.

Do not remove `.gitkeep` from directories that must remain empty and tracked.

Run the full suite:

`pytest ml/tests/ -v`

All 37 pre-existing tests must pass. Add tests for newly extracted modules and artifact backward compatibility where necessary.

Also verify:
- Fresh-clone startup using committed artifacts.
- Live and readiness health endpoints.
- Single and batch predictions.
- Existing educational disclaimer, exactly:

"PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."

- No training is triggered during inference.
- No database or backend dependency is introduced into the ML service.

## Restrictions

- Do not modify Phase 4 Spring Boot backend files or start Phase 4 implementation.
- Do not retrain or replace the model merely to accommodate a module move.
- Do not change model behavior, API contracts, dependency versions, or environment-variable names without identifying a proven necessity and reporting it.
- Do not modify the dataset or its provenance disclaimer.
- Do not use Docker for local development.
- Do not commit, push, reset, or discard user changes.
- Preserve existing unrelated modifications, including `AGENTS.md` and `prompts/phase4.md`.
- Inspect Git status before editing and again afterward.
- If a regression cannot be resolved safely, stop and report the failure rather than deleting compatibility code or weakening tests.

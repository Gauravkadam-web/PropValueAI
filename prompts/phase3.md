# Antigravity IDE Prompt — Phase 3: FastAPI ML Inference Service

## Project: PropValueAI — Real Estate Price Prediction

Phase 0, Phase 1, and Phase 2 are complete. The Phase 2 independent audit has declared the project ready for Phase 3.

Implement **Phase 3 only: the Python FastAPI inference service** that loads the existing fitted scikit-learn pipeline and exposes prediction endpoints.

The project is an educational ML demonstration. Its dataset uses mapped Pune locality labels and MUST NOT be represented as genuine Pune market valuation data.

## 1. Inspect Before Implementing

Read and follow:

- `AGENTS.md`
- `README.md`
- `docs/architecture.md`
- `docs/development-roadmap.md`
- `docs/api-contracts.md`
- `docs/dataset-evaluation.md`
- `docs/dataset-validation-report.md`
- `docs/model-training-report.md`
- `ml/README.md`
- `ml/training/README.md`
- `ml/common/constants.py`
- `ml/common/transformers.py`
- `ml/inference/artifacts/metadata.json`

Inspect the actual saved artifact and the existing ML code.

Before making changes:

1. Check the Git branch and working-tree status.
2. Inspect existing inference directories and files.
3. Confirm the local model artifact exists.
4. Confirm that metadata matches the artifact's expected feature schema and target units.
5. Check the installed FastAPI, Pydantic, Python, and scikit-learn versions.
6. Read the API contract and reuse its agreed request and response structures wherever defined.

Do not guess the model's feature schema. Derive it from the existing pipeline, metadata, and documentation.

## 2. Service Responsibilities

Implement a standalone FastAPI service responsible only for:

- Loading the fitted model pipeline.
- Validating incoming property data.
- Performing inference using the loaded pipeline.
- Returning structured predictions.
- Providing health and readiness checks.
- Reporting meaningful validation and inference errors.

The service must not train or retrain models.

The service must not own application business logic, authentication, user accounts, prediction history, or PostgreSQL access.

In the final architecture, the Spring Boot backend will orchestrate application requests and call the internal FastAPI inference service. For this phase, the service must be independently testable.

## 3. Suggested File Structure

Follow the existing repository conventions. Use the following layout if it fits the existing structure:

`ml/inference/`
- `app/__init__.py`
- `app/main.py`
- `app/schemas.py`
- `app/predictor.py`
- `app/config.py`
- `tests/` or the existing appropriate test location

Do not duplicate existing modules or introduce unnecessary package layers.

Place new tests under the existing ML test structure where appropriate.

## 4. Model Loading and Lifecycle

Implement reliable model loading.

Requirements:

- Load the existing `ml/inference/artifacts/model.joblib` artifact from a configurable path.
- Resolve the default artifact path reliably, independent of the current working directory.
- Allow an environment variable to override the model artifact path.
- Load the model once during application startup or lifespan initialization, not once per request.
- Keep the loaded pipeline available for subsequent requests.
- Verify that the artifact is fitted and compatible with the expected input schema.
- Check metadata consistency and expose the model version where available.
- Handle a missing, corrupt, or incompatible artifact without crashing silently.
- If loading fails, the readiness endpoint must indicate that inference is unavailable.
- Do not create a fake model or silently fall back to an untrained estimator.
- Do not download model files at runtime.

Use the current installed environment and declared dependencies. If a compatibility problem is found, report it and propose the smallest justified correction rather than retraining or silently changing the artifact.

## 5. Request Validation

Implement Pydantic request schemas based on the actual feature contract.

Support the feature inputs required by the existing fitted pipeline, including the applicable property-area, bedroom, bathroom, balcony, and area-type fields.

Inspect `PropertyFeatureTransformer` to determine which inputs should accept numeric values, strings, optional values, or missing values.

Requirements:

- Accept legitimate numeric and textual input formats supported by the existing transformer.
- Validate required fields and reject malformed input with clear errors.
- Handle missing optional values according to the established preprocessing contract.
- Reject NaN, positive infinity, negative infinity, and invalid numeric values where applicable.
- Apply sensible input validation without introducing unsupported assumptions about property values.
- Preserve area units and textual area formats according to the existing transformer.
- Do not accept `price` as a prediction feature.
- Do not require `site_location`, `society`, or `availability` if the trained pipeline excludes them.
- Do not introduce a locality-based prediction feature.
- Avoid silently coercing invalid input into a plausible property measurement.

Do not rebuild preprocessing in the API. Reuse the saved pipeline.

## 6. Prediction Endpoints

Implement endpoints consistent with `docs/api-contracts.md`.

At minimum, provide:

### `GET /health/live`

Returns a simple liveness response indicating that the process is running.

This endpoint must not claim the model is ready if model loading has failed.

### `GET /health/ready`

Reports whether the model artifact is successfully loaded and the service can perform inference.

Return an appropriate non-success HTTP status when the service is not ready.

### `POST /api/v1/predict`

Accepts a single property prediction request.

The response should contain, where supported by existing contracts:

- A prediction identifier only if the contract requires one and its generation is justified.
- The predicted property price.
- The target unit: Lakhs of Indian Rupees.
- Model name or version from verified metadata.
- A clear educational-demonstration limitation.

Do not generate fake user IDs, database records, or prediction history.

### `POST /api/v1/predict/batch`

Implement batch inference only if consistent with the API contract and practical for the local environment.

Validate batch size with a documented upper limit, return predictions in the same order as inputs, and provide clear errors for invalid requests.

Do not create unnecessary endpoints beyond this scope.

## 7. Prediction Semantics

The saved model predicts `price` in Lakhs of INR.

Ensure:

- Predictions are returned in Lakhs of INR.
- Do not multiply the model output by 100,000 unless a separately documented API field explicitly requires INR.
- Predictions must be finite numbers.
- Apply a non-negative prediction policy only if it is compatible with the project's documented target semantics; if applied, document it.
- Do not claim estimates are certified, current, or accurate for the real Pune market.
- Include or expose this disclaimer in the service's prediction contract:

  "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."

## 8. Error Handling and Logging

Implement clear, consistent HTTP errors for:

- Invalid request data.
- Model not ready.
- Prediction failures.
- Invalid batch requests.
- Unexpected internal errors.

Do not expose stack traces, local filesystem paths, secrets, or environment values in public responses.

Use appropriate server-side logging without logging unnecessary full property payloads or sensitive information.

Do not catch every exception and return a successful response.

## 9. Security and Configuration

- Keep configuration environment-driven where appropriate.
- Do not hardcode credentials or secrets.
- Do not add authentication or authorization in this phase; those responsibilities belong to the application architecture and later integration work.
- Do not expose arbitrary filesystem paths through request parameters.
- Do not permit user input to select or load arbitrary model files.
- Do not add broad CORS permissions without an actual requirement.
- Do not expose production debug mode.
- Do not add database connections.

## 10. Tests

Write meaningful automated tests for:

- Successful model loading.
- Missing or invalid artifact behavior.
- Readiness before and after successful initialization.
- Valid single prediction.
- Valid batch prediction, if implemented.
- Request schema validation.
- Numeric and textual area inputs supported by the transformer.
- Missing optional fields.
- Invalid numbers, NaN, and infinity.
- Finite predictions and correct target units.
- Consistent single-versus-batch predictions.
- Model loading only once per application lifecycle.
- Error responses when inference fails.
- Educational disclaimer and metadata consistency.

Use the existing fitted artifact for integration tests where available.

Unit tests may mock the predictor where appropriate, but do not use mocks as the only evidence that real inference works.

Tests must not depend on network access.

## 11. Local Development

Local development must remain Docker-free.

Document the exact Windows PowerShell commands to:

1. Activate the existing virtual environment.
2. Install only the required dependencies, if missing.
3. Start the FastAPI service using Uvicorn.
4. Open the Swagger UI.
5. Check liveness and readiness.
6. Submit a sample prediction.
7. Run the inference tests.

Do not install or introduce Docker, Docker Compose, PostgreSQL, Spring Boot, or Next.js for this phase.

## 12. Documentation

Create or update:

- `ml/inference/README.md`
- `docs/api-contracts.md`, only where necessary to document actual implemented endpoints and schemas.
- `ml/README.md`, only if needed to explain the inference workflow.

Document endpoint paths, example requests and responses, target units, validation behavior, readiness behavior, configuration variables, startup commands, and known limitations.

Do not claim that future Spring Boot integration has been completed.

## 13. Git and Scope Discipline

- Preserve all existing work.
- Do not delete or reset files.
- Do not stage, commit, or push.
- Do not modify the Git remote.
- Do not retrain or overwrite the Phase 2 model artifact.
- Keep the raw dataset, virtual environment, generated plots, and ML artifacts excluded from Git as intended.
- Do not implement Spring Boot, Next.js, database persistence, authentication, or deployment.
- Do not begin Phase 4.

## 14. Final Report and Stop Condition

At completion, report:

1. Files created or modified.
2. Implemented endpoints and schemas.
3. Model-loading behavior and artifact compatibility.
4. Actual tests executed and results.
5. Exact local startup and testing commands.
6. Any issues or unresolved limitations.
7. Git status and diff summary.
8. Confirmation that the existing model was not retrained or overwritten.

Stop after Phase 3 and wait for explicit approval before starting Phase 4.

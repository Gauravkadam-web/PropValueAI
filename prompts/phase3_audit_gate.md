# Antigravity Audit Prompt — PropValueAI Phase 3 Review Gate

You are auditing **PropValueAI — Real Estate Price Prediction Using Python and Machine Learning**.

Phase 3 implements the standalone FastAPI ML inference service. The implementation report claims 37 tests passed, live prediction succeeded, and the Phase 2 trained model was preserved.

## Objective

Perform an independent, evidence-based audit of the actual repository. Verify the implementation rather than trusting the previous report.

**This is an audit-only task. Do not modify code, dependencies, documentation, configuration, Git history, or model artifacts. Do not commit or push. Do not start Phase 4.**

## 1. Read Project Instructions and Contracts

Read:
- `AGENTS.md`
- `README.md`
- `docs/architecture.md`
- `docs/development-roadmap.md`
- `docs/api-contracts.md`
- `docs/dataset-validation-report.md`
- `docs/model-training-report.md`
- `ml/README.md`
- `ml/training/README.md`
- `ml/inference/README.md`
- `prompts/phase3.md`

If any listed file is absent, report that fact instead of assuming its contents.

## 2. Inspect the Actual Implementation

Review these files:
- `ml/inference/app/config.py`
- `ml/inference/app/schemas.py`
- `ml/inference/app/predictor.py`
- `ml/inference/app/main.py`
- `ml/inference/main.py`
- `ml/inference/requirements.txt`
- `ml/tests/test_inference_api.py`
- Existing tests under `ml/tests/`
- `.gitignore`

Check for the following:

### Model loading and readiness
- The existing Phase 2 fitted pipeline and metadata are loaded from deterministic, CWD-independent paths.
- Environment-variable overrides work as documented.
- The model is loaded once per application process during lifespan initialization, not once per prediction.
- Missing, corrupt, or incompatible artifacts produce a controlled unready state and prediction responses return HTTP 503.
- The readiness endpoint does not report ready unless the model is actually usable.
- No runtime model training, external model download, or silent fallback to a dummy model occurs.
- The audit does not retrain, regenerate, or overwrite the Phase 2 model artifact.

### Request validation and model compatibility
- Request fields match the actual features expected by the fitted pipeline and its transformers.
- The `price` target is rejected when supplied in a prediction request.
- Unsupported fields are handled consistently with the documented contract.
- Numeric and string `total_sqft` inputs are normalized safely.
- Non-positive area, malformed strings, NaN, infinity, negative bathroom/balcony values, and unreasonable bathroom counts are handled as intended.
- Missing optional inputs are processed by the existing fitted preprocessing pipeline.
- Unseen categorical values are handled safely.
- Single and batch predictions preserve order and return equivalent values for equivalent inputs.
- Batch size limits are enforced before expensive inference.

### Prediction correctness
- Predictions are finite and non-negative.
- The target and response units are consistently **Lakhs INR**, with no accidental extra multiplication or division by 100,000.
- The model version and metadata returned by `/api/v1/model-info` reflect the actual artifact metadata rather than fabricated values.
- The required educational disclaimer is present in every prediction response.
- The disclaimer accurately communicates that estimates are simulated educational outputs, not actual Pune market valuations.

### API and operational behavior
Verify the documented behavior of:
- `GET /`
- `GET /health/live`
- `GET /health/ready`
- `GET /api/v1/model-info`
- `POST /api/v1/predict`
- `POST /api/v1/predict/batch`

Check status codes, response schemas, error handling, startup commands, logging, and absence of unintended database, authentication, broad CORS, or unrelated Phase 4 functionality.

### Dependencies and reproducibility
- Check whether `ml/inference/requirements.txt` declares compatible, appropriate versions for the actual code.
- Check for dependency conflicts with the existing project virtual environment and Phase 2 ML stack.
- Determine whether test-only dependencies such as `httpx` are correctly justified.
- Do not upgrade packages or install dependencies during the audit.
- Confirm whether the ignored model artifact and metadata are available locally and explain how their exclusion from Git affects reproducibility and future deployment. Do not change `.gitignore`.

## 3. Run Tests

Use the existing project virtual environment and run:

```powershell
& ".\.venv\Scripts\pytest.exe" ml/tests/ -v
```

If the path differs, inspect the environment and use the correct existing executable. Do not create a new environment or install packages.

Report the actual exit code, passed/failed/skipped counts, and any warnings or errors. Do not claim tests passed if the command did not complete successfully.

If feasible without modifying project files, perform a read-only live smoke test against an already running service. Do not launch competing servers if port 8000 is occupied. Clearly distinguish actual live checks from automated test-client checks.

## 4. Git and Artifact Safety

Inspect `git status --short`, current branch, and recent commit history.

Confirm:
- No files were modified by the audit.
- No files were staged, committed, or pushed.
- No model artifact was regenerated or overwritten.
- Existing user changes were preserved.

Do not delete, reset, stash, or clean anything.

## 5. Required Audit Report

Provide `docs/phase3-audit-report.md` as a **proposed report in your response only**; because this task is read-only, do not create or modify the file.

Include:
1. Executive verdict: `PASS`, `PASS WITH NON-BLOCKING FINDINGS`, or `FAIL`.
2. Files and contracts inspected.
3. Actual test command and results.
4. Findings categorized as Critical, High, Medium, Low, or None.
5. Evidence for each finding: file path, relevant function or line numbers where available, and concrete impact.
6. Endpoint and validation review.
7. Model-loading, metadata, and artifact-reproducibility review.
8. Git safety confirmation.
9. Explicit recommendation: fix issues first or approve Phase 3.

Do not report a concern as a confirmed defect without evidence. If something cannot be verified, mark it **Unverified** and explain why.

## Stop Condition

Stop after presenting the audit report. Do not implement fixes, commit/push, or begin Phase 4 (Spring Boot Backend Core). Await explicit authorization.

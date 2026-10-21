# AI Development Instructions — Real Estate Price Prediction

## 1. Project purpose
Build a maintainable real-estate price prediction web application using Next.js, Spring Boot, Python FastAPI, PostgreSQL, and scikit-learn. Follow the approved project documentation.

## 2. Phase discipline
- Work only on the phase and task explicitly requested by the project owner.
- Before changing files, inspect the current repository, relevant documentation, Git status, and existing implementation.
- For significant tasks, first present a concise plan and list the files expected to change.
- Do not silently expand scope or start future phases.
- At completion, report files changed, commands run, actual test results, unresolved issues, and next steps.
- Never claim a test passed unless it was actually run and passed.

## 3. Finalized technology choices
- Frontend: Next.js, TypeScript, Tailwind CSS
- Core backend: Java 21, Spring Boot, Spring Data JPA/Hibernate
- ML inference: Python, FastAPI
- Database: PostgreSQL
- Database migrations: Flyway
- ML: pandas, NumPy, scikit-learn, joblib
- Version control: Git and GitHub

Do not substitute frameworks or introduce infrastructure without asking the owner.

## 4. Architecture boundaries
- Next.js browser clients call Spring Boot application APIs.
- Spring Boot owns application business logic, authentication, authorization, input validation, prediction history, and primary application database access.
- Spring Boot calls the internal Python FastAPI inference service.
- FastAPI loads the approved saved model artifact and performs inference only.
- ML training and evaluation are offline tasks; never retrain on each prediction request.
- PostgreSQL is accessed primarily through Spring Boot. Do not create a second database owner in the ML service without explicit approval.
- Keep service contracts documented and consistent.

## 5. ML correctness
- Inspect and validate real datasets before finalizing target columns, feature lists, units, or input schemas.
- The two candidate datasets are not approved until inspected.
- Do not merge datasets without checking geographic coverage, price meaning, currency, area units, dates, schema, quality, and licensing.
- Preserve raw source data unchanged.
- Split data before fitting learned preprocessing; avoid leakage from held-out test data.
- Use a fitted scikit-learn Pipeline/ColumnTransformer where suitable so training and inference transformations match.
- Start with a baseline such as Linear Regression, then compare appropriate alternatives using a valid evaluation strategy.
- Report MAE, RMSE, and R² with context; R² is not a percentage accuracy score.
- Never fabricate datasets, evaluation metrics, model outputs, or model artifacts.
- Generate `model.joblib` and `metadata.json` only after an actual successful training/evaluation workflow.
- Load joblib/pickle artifacts only from trusted sources.
- Keep training and inference dependency versions compatible.

## 6. Structure preservation
Preserve the agreed repository structure:
- `frontend/`
- `backend/`
- `ml/training/`
- `ml/inference/`
- `ml/pipeline/`
- `ml/common/`
- `ml/tests/`
- `docs/`

Within `ml/training/`, preserve `data/raw/`, `data/processed/`, `data/external/`, `scripts/`, `experiments/`, and `requirements.txt`.
Within `ml/inference/`, preserve `model/`, `preprocessing/`, `services/`, `artifacts/`, `config/`, and the future FastAPI entry point.
Do not rename or reorganize these paths without explaining why and receiving approval. Empty directories may use `.gitkeep`.

Avoid duplicate preprocessing logic. `preprocess.py` and `pipeline.py` are optional implementation modules: add them only when they have a clear, non-duplicative responsibility. Keep optional `generate_data.py` limited to clearly labelled test/demo data; never use synthetic data to claim real-world model quality.

## 7. Security and configuration
- Never hardcode passwords, tokens, API keys, database credentials, hostnames, or environment-specific secrets.
- Use environment variables and documented example environment files with placeholder values only.
- Never commit `.env` files containing secrets.
- Implement authorization checks server-side; do not rely on frontend hiding controls.
- Validate types, ranges, units, and unexpected inputs at service boundaries.
- Return safe errors; do not expose stack traces or secrets to end users.
- Avoid unnecessary dependencies and infrastructure.

## 8. Development environment and deployment
- Local development should not require Docker.
- Docker is reserved for the planned production/deployment phase.
- Do not install dependencies, create virtual environments, run migrations, or download datasets unless the current task calls for it.
- Use Windows-compatible commands when providing local setup instructions, unless the owner asks otherwise.

## 9. Git safety
- Inspect `git status`, current branch, and remotes before Git operations.
- Never assume the remote repository is empty.
- Never change an existing remote, rewrite history, force-push, reset, delete, or overwrite user work without explicit approval.
- Do not commit or push unless explicitly authorized by the project owner.
- Never include credentials or private datasets in commits.

## 10. Phase 0 restriction
During Phase 0, create/review only the agreed folder structure and documentation. Do not implement frontend pages, backend application code, database connections/migrations, ML training, model artifacts, or working inference endpoints.

## 11. Definition of done
A task is done only when:
1. The requested scope is implemented without unrelated changes.
2. The resulting files are inspected.
3. Relevant checks/tests are actually run when applicable.
4. Documentation reflects the real state, not intended future behavior.
5. Results and known limitations are reported truthfully.

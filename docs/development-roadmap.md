# Development Roadmap

**Project:** Real Estate Price Prediction Using Python and ML  
**Status:** Phase 0 — foundation and documentation.

Each phase requires review and verification before starting the next. The phases are a plan, not a claim that work is complete.

## Phase 0 — Project foundation
**Scope**
- Preserve the agreed repository structure.
- Add `AGENTS.md`, root and ML README files, architecture, roadmap, and preliminary API-contract documentation.
- Inspect local Git state and remote configuration safely.
- Define coding, security, testing, and phase boundaries.

**Acceptance criteria**
- Documentation agrees on the stack and architecture.
- No application functionality or model training has been implemented.
- Git history/remotes and existing files are preserved.
- Any Git commit/push requires explicit owner approval.

## Phase 1 — Dataset inspection and validation
**Scope**
- Obtain candidate dataset files from legitimate sources.
- Record provenance, license, download/reference date, columns, row counts, types, missing values, duplicates, outliers, price definition, currency, area units, and geographic coverage.
- Compare candidates for schema and semantic compatibility.
- Decide whether to use one dataset or combine sources.

**Acceptance criteria**
- A dataset inspection report is available.
- The target column and candidate features are grounded in actual data.
- Data licensing and repository-size considerations are documented.
- No merge is performed without evidence of compatibility.

## Phase 2 — EDA, preprocessing, training, and evaluation
**Scope**
- Perform exploratory analysis and document assumptions.
- Establish an appropriate train/validation/test strategy.
- Prevent leakage by fitting learned transformations only on training data.
- Build a scikit-learn Pipeline/ColumnTransformer where appropriate.
- Train a baseline such as Linear Regression, then compare suitable alternatives.
- Evaluate MAE, RMSE, and R² and review residuals/errors.
- Save the selected fitted pipeline and metadata only after a real successful run.

**Acceptance criteria**
- Training and evaluation are reproducible.
- Final test data was not used for fitting or model selection.
- Metrics identify the dataset/model version and are not fabricated.
- A trusted `.joblib` artifact and metadata are generated.

## Phase 3 — FastAPI inference service
**Scope**
- Implement model loader, predictor, prediction service, runtime settings, and FastAPI entry point.
- Load the artifact at startup or through an intentional model lifecycle.
- Validate request features against the final training contract.
- Provide health, model-info, and predict endpoints after schemas are approved.
- Add tests for valid/invalid inputs and serialization round trips.

**Acceptance criteria**
- API predictions use the saved pipeline.
- No per-request retraining occurs.
- Training/inference transformations and dependency versions are compatible.
- Errors are safe and actionable.

## Phase 4 — Spring Boot backend
**Scope**
- Set up Java 21 and Spring Boot application.
- Design database entities and schema based on approved requirements.
- Add Flyway migrations and PostgreSQL configuration.
- Implement authentication, authorization, validation, prediction orchestration, history, and admin operations as scoped.
- Document REST APIs.
- Integrate with FastAPI through an internal service client.

**Acceptance criteria**
- Migrations work on a clean local database.
- Protected endpoints enforce server-side authorization.
- Prediction and history flows have automated tests.
- Secrets/configuration are environment-driven.

## Phase 5 — Next.js frontend
**Scope**
- Create accessible, responsive UI with TypeScript and Tailwind CSS.
- Implement account screens, property input form, results, history, and admin screens according to approved requirements.
- Integrate only with Spring Boot APIs.
- Handle loading, validation, empty, success, and error states.

**Acceptance criteria**
- Main flows work against the real backend.
- No mock result is represented as a real ML prediction.
- Role-specific UI is backed by server-side authorization.

## Phase 6 — Integration, security, and end-to-end testing
**Scope**
- Test browser-to-backend-to-ML-to-database prediction flow.
- Verify data ownership, authentication, authorization, error handling, validation, model version tracking, and prediction history.
- Run unit, integration, and frontend tests.
- Fix issues and document known limitations.

**Acceptance criteria**
- Key user and admin flows pass reproducible tests.
- Failed dependencies and invalid input fail safely.
- ML metrics and test results are reported truthfully.

## Phase 7 — Production preparation and deployment
**Scope**
- Select deployment providers and configure environments.
- Package services with Docker for production only if approved.
- Configure managed PostgreSQL, secrets, health checks, logging, and backups.
- Document deployment, rollback, and model artifact update process.

**Acceptance criteria**
- Production setup is reproducible and documented.
- No secrets are committed.
- Model artifacts are trusted and versioned.
- Operational limitations and costs are documented.

## Phase completion protocol
For every phase:
1. Inspect the repository and Git state.
2. Present a plan before significant changes.
3. Implement only the approved scope.
4. Run applicable checks and tests.
5. Review changed files and update documentation.
6. Report actual results and unresolved issues.
7. Wait for approval before the next phase or Git commit/push.

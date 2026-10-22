# PropValueAI — Phase 4 Spring Boot Backend Implementation Prompt

Repository: https://github.com/Gauravkadam-web/PropValueAI
Local project directory: D:\PropValueAI

Implement Phase 4: Spring Boot Backend according to the approved project architecture and prompts/phase4.md.

## 1. Mandatory rules
- Read AGENTS.md, README.md, docs/architecture.md, docs/development-roadmap.md, docs/api-contracts.md, ml/README.md, ml/inference/README.md, and prompts/phase4.md before making changes.
- Treat the existing approved architecture and Phase 4 specification as authoritative.
- Do not redesign, reorganize, rename, or refactor the existing ML architecture.
- Do not modify ML training, inference, pipeline, common modules, model artifacts, dataset, or existing ML behavior.
- Do not implement Phase 5 frontend or Phase 7 Docker deployment.
- Do not commit, push, reset, or discard any Git changes.
- Inspect the current Git status before editing. Preserve unrelated user changes.
- Verify dependency versions and compatibility before selecting them. Prefer Spring Boot dependency management rather than independently overriding Spring component versions.
- Never hardcode credentials, JWT secrets, database passwords, or environment-specific URLs.
- Do not claim a test passed unless you actually ran it and observed the result.

## 2. Approved architecture
- Java 21
- Spring Boot backend (3.3.x)
- Spring Web
- Spring Data JPA
- Spring Security
- JWT-based authentication
- BCrypt password hashing
- PostgreSQL
- Flyway database migrations
- FastAPI as an internal ML inference service
- Maven
- OpenAPI/Swagger documentation

Architecture boundaries:
- The browser/frontend communicates only with Spring Boot.
- Spring Boot owns authentication, authorization, application business logic, PostgreSQL access, and prediction history.
- FastAPI is used only by Spring Boot for ML inference.
- FastAPI must not be given responsibility for users, authentication, PostgreSQL persistence, or prediction history.
- Preserve the existing ML module folder structure and public inference API contract.
- Expected Java package root: `com.propvalueai.backend`.

## 3. Authentication and authorization
- User registration (`POST /api/v1/auth/register`)
- User login (`POST /api/v1/auth/login`)
- Current user profile (`GET /api/v1/auth/me`)
- JWT authentication filter & token provider
- BCrypt password hashing
- Every prediction requires an authenticated user. Guest predictions are prohibited.
- Public registration assigns `ROLE_USER` (cannot register as admin).
- Admin provisioning via configuration / operational seed.
- Users can access only their own prediction records.
- Admin access restricted with `@PreAuthorize("hasRole('ADMIN')")`.

## 4. Database and migrations
- PostgreSQL with Flyway-managed schema migrations (`V1__init_schema.sql`).
- Minimum schema: `users`, `prediction_records`.
- User entity: ID, email (unique), password_hash, first_name, last_name, role, created_at, updated_at.
- Prediction record entity: ID, user_id (FK), total_sqft_input, size_input, bath_input, balcony_input, area_type_input, predicted_price_lakhs, target_unit, model_name, model_version, fastapi_prediction_id, disclaimer, status, created_at.

## 5. FastAPI integration
- Spring 6 `RestClient`.
- Configuration via `PROPVALUEAI_FASTAPI_BASE_URL` (default: `http://127.0.0.1:8000`).
- Configured connection and read timeouts.
- Pre-validation of inputs before calling FastAPI.
- Graceful handling of timeouts, 422 validation errors, and 503 unavailable states.
- Mandatory disclaimer:
  "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."

## 6. Endpoints
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/predictions`
- `POST /api/v1/predictions/batch`
- `GET /api/v1/predictions` (paginated, user-isolated)
- `GET /api/v1/predictions/{id}` (ownership check)
- `GET /api/v1/admin/predictions` (admin only, paginated)
- `GET /api/v1/health`
- `/swagger-ui/**`, `/v3/api-docs/**`

## 7. Testing
- Unit tests, MockMvc controller slice tests, DataJpa repository tests, and RestClient tests using `MockRestServiceServer`.
- Full regression check of ML test suite (`pytest ml/tests/ -v`).

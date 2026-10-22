# PropValueAI — Phase 4: Spring Boot Backend
## Implementation Plan & Pre-Implementation Audit

**Project:** PropValueAI — Real Estate Price Prediction Web Application  
**Target Repository:** `D:\PropValueAI`  
**GitHub:** `https://github.com/Gauravkadam-web/PropValueAI.git`  
**Phase:** Phase 4 — Core Spring Boot Backend Service  
**Date:** October 22, 2026  
**Status:** Pre-Implementation Plan (Audit & Architecture Gate) — **Awaiting Approval Before Implementation**

---

## 1. Verified Current Repository State

### 1.1 Git Status & Workspace Verification
- **Current Branch:** `main` (synchronized with `origin/main` at commit `099d8f0`).
- **Working Tree:** 100% clean, no uncommitted changes, no untracked file conflicts.
- **Repository Directory:** `backend/` exists as a preserved placeholder directory containing `.gitkeep`.
- **Existing Rules & Discipline:** `AGENTS.md` mandates that all application business logic, persistence, authorization, and prediction history belong exclusively to Spring Boot. FastAPI is an internal inference worker and must never own the database.

### 1.2 Local Development Environment & Toolchains (Windows)
- **Java Runtime:** `Java 21.0.8 LTS` verified (`java version "21.0.8" 2025-07-15 LTS`).
- **Build Tool:** `Apache Maven 3.9.16` verified (`mvn -v` functional in system PATH).
- **Database:** `PostgreSQL 18.0` verified running on `localhost:5432` (`postgresql-x64-18` Windows service active).
- **ML Inference Service (Phase 3):** Python FastAPI service functional, verified by 37 passing unit/API tests (`ml/tests/`). Model artifact `model.joblib` and `metadata.json` are committed and tracked under `ml/inference/artifacts/`.
- **Docker Policy:** Docker-free local development strictly observed (Docker reserved for Phase 7).

### 1.3 Verified Phase 3 Inference Contracts
Direct inspection of `ml/inference/app/main.py` and `ml/inference/app/schemas.py` confirms:
- **Endpoints:**
  - `GET /health/live`: Process liveness check (`{"status": "alive", "service": "propvalueai-inference"}`).
  - `GET /health/ready`: Pipeline readiness check (`200 OK` when model loaded; `503 Service Unavailable` if uninitialized).
  - `GET /api/v1/model-info`: Architectural metadata, feature schema, and evaluation metrics.
  - `POST /api/v1/predict`: Single prediction endpoint.
  - `POST /api/v1/predict/batch`: Batch prediction endpoint (1 to 100 properties).
- **Input Feature Schema (`PropertyPredictRequest`):**
  - `total_sqft` (Required): Positive float, int, or valid range/unit string (`"2100 - 2850"`, `"1000Sq. Meter"`).
  - `size` / `bhk` (Optional): Bedroom specification string or direct integer.
  - `bath` (Optional): Bathroom count float ($0.0 \le bath \le 20.0$).
  - `balcony` (Optional): Balcony count float ($0.0 \le balcony \le 10.0$).
  - `area_type` (Optional): String category (`"Super built-up  Area"`, `"Plot  Area"`, `"Built-up  Area"`, `"Carpet  Area"`).
  - Target variable `price` is **strictly forbidden** (rejected with HTTP `422 Unprocessable Entity` to prevent data leakage).
- **Output Schema (`PropertyPredictResponse`):**
  - `prediction_id`: UUID string.
  - `predicted_price`: Non-negative float in Lakhs INR.
  - `target_unit`: `"Lakhs INR"`.
  - `model_name`: `"Random Forest"`.
  - `model_version`: `"1.0.0"`.
  - `disclaimer`: Mandatory text:
    > *"PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."*

---

## 2. Proposed Backend Architecture & Package Structure

The backend will be structured as a standard Maven multi-layer modular architecture under `backend/`, following Spring Boot conventions:

```text
backend/
├── pom.xml                                      # Maven project configuration
├── mvnw / mvnw.cmd                              # Maven wrapper scripts
├── .mvn/wrapper/                                # Maven wrapper binary and properties
└── src/
    ├── main/
    │   ├── java/com/propvalueai/backend/
    │   │   ├── BackendApplication.java          # Spring Boot main entrypoint
    │   │   ├── config/                          # Configuration beans
    │   │   │   ├── SecurityConfig.java          # Spring Security 6 filter chain, CORS, password encoder
    │   │   │   ├── RestClientConfig.java        # Spring 6 RestClient for FastAPI server-to-server calls
    │   │   │   ├── OpenApiConfig.java           # Swagger / OpenAPI 3 specifications & metadata
    │   │   │   └── AppProperties.java           # Type-safe @ConfigurationProperties
    │   │   ├── controller/                      # REST API Controllers
    │   │   │   ├── AuthController.java          # Registration, login, profile me endpoints
    │   │   │   ├── PredictionController.java    # Single & batch prediction, user history endpoints
    │   │   │   ├── AdminPredictionController.java # Admin-only prediction history & stats
    │   │   │   └── HealthController.java        # Spring Boot health + downstream dependency probe
    │   │   ├── dto/                             # Request and Response Data Transfer Objects
    │   │   │   ├── auth/
    │   │   │   │   ├── RegisterRequest.java     # Email, password, first name, last name
    │   │   │   │   ├── LoginRequest.java        # Email, password
    │   │   │   │   ├── AuthResponse.java        # JWT token, expiration, user info
    │   │   │   │   └── UserProfileResponse.java # Authenticated user details
    │   │   │   ├── prediction/
    │   │   │   │   ├── PropertyInputRequest.java # Validated property input for prediction
    │   │   │   │   ├── BatchPropertyInputRequest.java # List of 1-100 property inputs
    │   │   │   │   ├── PredictionResponse.java  # Predicted price, disclaimer, record ID
    │   │   │   │   ├── BatchPredictionResponse.java # List of prediction results
    │   │   │   │   ├── PredictionHistoryResponse.java # User history record with timestamp
    │   │   │   │   └── FastApiPredictRequest.java # Outgoing DTO to FastAPI service
    │   │   │   └── common/
    │   │   │       ├── ApiErrorResponse.java    # Standardized error envelope
    │   │   │       └── PageResponse.java        # Standardized paginated metadata envelope
    │   │   ├── entity/                          # JPA Entities
    │   │   │   ├── UserEntity.java              # Users table entity
    │   │   │   ├── Role.java                    # Enum: ROLE_USER, ROLE_ADMIN
    │   │   │   └── PredictionRecordEntity.java  # Prediction history records table entity
    │   │   ├── exception/                       # Custom exceptions and global advice
    │   │   │   ├── GlobalExceptionHandler.java  # @RestControllerAdvice for validation, 401, 403, 404, 503
    │   │   │   ├── ResourceNotFoundException.java
    │   │   │   ├── DuplicateResourceException.java
    │   │   │   ├── InferenceServiceException.java # Handles FastAPI unreachable or 5xx states
    │   │   │   └── UnauthorizedException.java
    │   │   ├── repository/                      # Spring Data JPA Repositories
    │   │   │   ├── UserRepository.java          # findByEmail, existsByEmail
    │   │   │   └── PredictionRecordRepository.java # findByUserId, findAll with specifications
    │   │   ├── security/                        # Security implementation components
    │   │   │   ├── JwtTokenProvider.java        # JWT generation, signature parsing, expiration check
    │   │   │   ├── JwtAuthenticationFilter.java # OncePerRequestFilter for Bearer token validation
    │   │   │   ├── SecurityUserPrincipal.java   # UserDetails implementation
    │   │   │   └── CustomUserDetailsService.java # Loads user from UserRepository
    │   │   └── service/                         # Business Logic & Orchestration
    │   │       ├── AuthService.java             # Register, authenticate, generate tokens
    │   │       ├── PredictionService.java       # Orchestrates: Validate -> Call FastAPI -> Save Record -> Return DTO
    │   │       ├── PredictionHistoryService.java # User-isolated history & admin history querying
    │   │       └── FastApiClientService.java    # HTTP client communication with Python FastAPI service
    │   └── resources/
    │       ├── application.yml                  # Base configuration with environment overrides
    │       └── db/migration/
    │           └── V1__init_schema.sql          # Flyway baseline schema for users and predictions
    └── test/
        ├── java/com/propvalueai/backend/
        │   ├── BackendApplicationTests.java     # Context load test
        │   ├── auth/AuthControllerTest.java     # MockMvc auth slice test
        │   ├── prediction/PredictionControllerTest.java # MockMvc prediction & history test
        │   ├── service/FastApiClientServiceTest.java # MockRestServiceServer test for FastAPI client
        │   ├── repository/UserRepositoryTest.java # DataJpa test
        │   └── security/JwtTokenProviderTest.java # JWT generation and validation unit test
        └── resources/
            └── application-test.yml             # Test-specific profile (H2 or test PostgreSQL)
```

---

## 3. Dependency & Configuration Plan

### 3.1 Technology Stack & Versions
- **Java:** `21` (LTS)
- **Spring Boot:** `3.3.5` (Latest stable 3.3.x line; compatible with Java 21, Spring Security 6.3, Jakarta EE 10)
- **Database:** `PostgreSQL 18.0` (Local instance on port 5432)
- **Migration Engine:** `Flyway 10.x` (`flyway-core` + `flyway-database-postgresql`)
- **HTTP Client:** Spring 6 native `RestClient` (Lightweight, non-reactive, blocking HTTP client built into `spring-boot-starter-web`; eliminates WebFlux/Netty overhead)
- **Security & Tokens:** `Spring Security 6.3` with `jjwt-api`, `jjwt-impl`, `jjwt-jackson` (`0.12.6`)
- **API Documentation:** `springdoc-openapi-starter-webmvc-ui` (`2.6.0`)
- **Testing:** `spring-boot-starter-test` (JUnit 5, Mockito, AssertJ), `spring-security-test`, `H2` for lightweight unit/repository tests.

### 3.2 Key Dependencies (`pom.xml` Specification)
```xml
<dependencies>
    <!-- Web & Validation -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>

    <!-- Persistence & Flyway -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-core</artifactId>
    </dependency>
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-database-postgresql</artifactId>
    </dependency>

    <!-- Security & JWT -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-api</artifactId>
        <version>0.12.6</version>
    </dependency>
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-impl</artifactId>
        <version>0.12.6</version>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-jackson</artifactId>
        <version>0.12.6</version>
        <scope>runtime</scope>
    </dependency>

    <!-- OpenAPI 3 / Swagger Documentation -->
    <dependency>
        <groupId>org.springdoc</groupId>
        <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
        <version>2.6.0</version>
    </dependency>

    <!-- Testing -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

---

## 4. Database Entity & Flyway Migration Plan

Spring Boot exclusively owns application persistence. PostgreSQL will store user accounts and the complete audit history of predictions.

### 4.1 Flyway Migration: `V1__init_schema.sql`

```sql
-- Flyway Migration: V1__init_schema.sql
-- PropValueAI Core Application Schema

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'ROLE_USER',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS prediction_records (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    total_sqft_input VARCHAR(100) NOT NULL,
    size_input VARCHAR(50),
    bath_input DOUBLE PRECISION,
    balcony_input DOUBLE PRECISION,
    area_type_input VARCHAR(100),
    predicted_price_lakhs NUMERIC(12, 2) NOT NULL,
    target_unit VARCHAR(50) NOT NULL DEFAULT 'Lakhs INR',
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    fastapi_prediction_id VARCHAR(100),
    disclaimer TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'SUCCESS',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_predictions_user_id ON prediction_records(user_id);
CREATE INDEX idx_predictions_created_at ON prediction_records(created_at DESC);
```

### 4.2 JPA Entities
1. **`UserEntity`:**
   - Mapped to table `users`.
   - Fields: `id`, `email`, `passwordHash`, `firstName`, `lastName`, `role` (`Role.ROLE_USER`, `Role.ROLE_ADMIN`), `createdAt`, `updatedAt`.
2. **`PredictionRecordEntity`:**
   - Mapped to table `prediction_records`.
   - Fields: `id`, `user` (`@ManyToOne` nullable to support guest/demo predictions if allowed, or authenticated user), inputs (`totalSqftInput`, `sizeInput`, `bathInput`, `balconyInput`, `areaTypeInput`), outputs (`predictedPriceLakhs`, `targetUnit`, `modelName`, `modelVersion`, `fastapiPredictionId`, `disclaimer`, `status`, `createdAt`).

---

## 5. Authentication & Authorization Design

### 5.1 Authentication Flow
- **Registration (`POST /api/v1/auth/register`):**
  - Requires valid email, minimum 8-character password, first name, last name.
  - Checks uniqueness of email.
  - Hashes password using `BCryptPasswordEncoder` (strength 12).
  - Assigns default role `ROLE_USER`.
  - Returns user profile metadata (no password).
- **Login (`POST /api/v1/auth/login`):**
  - Authenticates credentials against database.
  - Generates HMAC-SHA256 signed stateless JWT with claims: `sub` (email), `role`, `userId`, `iat`, `exp` (default 24h).
  - Returns token and user summary.
- **Current User Profile (`GET /api/v1/auth/me`):**
  - Validates `Authorization: Bearer <token>`.
  - Returns the authenticated user's ID, email, name, and assigned roles.

### 5.2 Role-Based Access Control (RBAC) Matrix

| Endpoint | Method | Required Role | Description |
|---|---|---|---|
| `/api/v1/auth/register` | POST | Public | New user registration |
| `/api/v1/auth/login` | POST | Public | User authentication & JWT generation |
| `/api/v1/auth/me` | GET | `ROLE_USER` or `ROLE_ADMIN` | Current user profile |
| `/api/v1/predictions` | POST | Authenticated (or Public demo) | Predicts price, calls FastAPI, stores record |
| `/api/v1/predictions` | GET | `ROLE_USER` or `ROLE_ADMIN` | Returns **only the authenticated user's** history |
| `/api/v1/predictions/{id}` | GET | `ROLE_USER` or `ROLE_ADMIN` | Returns single record if owned by caller (or caller is admin) |
| `/api/v1/admin/predictions` | GET | `ROLE_ADMIN` | Paginated system-wide prediction history |
| `/api/v1/health` | GET | Public | Health probe (Spring Boot + PostgreSQL + FastAPI) |
| `/swagger-ui/**`, `/v3/api-docs/**` | GET | Public | OpenAPI documentation |

---

## 6. Endpoint Contracts & DTO Specifications

### 6.1 `POST /api/v1/predictions` (Single Prediction Request)

#### Request Body (`PropertyInputRequest`):
```json
{
  "total_sqft": 1056.0,
  "size": "2 BHK",
  "bath": 2.0,
  "balcony": 1.0,
  "area_type": "Super built-up  Area"
}
```

**Bean Validation Rules:**
- `total_sqft`: Required (`@NotNull`), positive numeric or non-empty string.
- `size`: Optional string or integer.
- `bath`: Optional float, `@Min(0)`, `@Max(20)`.
- `balcony`: Optional float, `@Min(0)`, `@Max(10)`.
- `area_type`: Optional string.
- Rejects any payload attempting to pass a target `price`.

#### Response Body (`PredictionResponse`) — `200 OK`:
```json
{
  "id": 142,
  "predicted_price": 55.20,
  "target_unit": "Lakhs INR",
  "model_name": "Random Forest",
  "model_version": "1.0.0",
  "fastapi_prediction_id": "98173fc5-ffeb-4373-8167-8e9d29d9ccaf",
  "disclaimer": "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.",
  "created_at": "2026-10-22T08:30:00Z"
}
```

### 6.2 `GET /api/v1/predictions` (User Prediction History)
- Query parameters: `page` (default 0), `size` (default 10), `sort` (default `createdAt,desc`).
- Enforces strict isolation: `SELECT * FROM prediction_records WHERE user_id = :currentUserId ORDER BY created_at DESC`.

#### Response Body (`PageResponse<PredictionHistoryResponse>`):
```json
{
  "content": [
    {
      "id": 142,
      "total_sqft": "1056.0",
      "size": "2 BHK",
      "bath": 2.0,
      "balcony": 1.0,
      "area_type": "Super built-up  Area",
      "predicted_price": 55.20,
      "target_unit": "Lakhs INR",
      "model_name": "Random Forest",
      "created_at": "2026-10-22T08:30:00Z"
    }
  ],
  "page": 0,
  "size": 10,
  "total_elements": 1,
  "total_pages": 1,
  "last": true
}
```

### 6.3 Standardized Error Envelope (`ApiErrorResponse`)
Returned on 400, 401, 403, 404, 422, 500, 503:
```json
{
  "timestamp": "2026-10-22T08:35:10Z",
  "status": 503,
  "error": "Service Unavailable",
  "message": "Inference service is currently unavailable. Please ensure the Python FastAPI engine is running.",
  "path": "/api/v1/predictions"
}
```

---

## 7. FastAPI Integration Design

### 7.1 Spring 6 `RestClient` Configuration
- `FastApiClientService` wraps `RestClient` with target base URL configured via `propvalueai.ml.inference-url` (default: `http://127.0.0.1:8000`).
- **Timeouts:**
  - Connection timeout: 3 seconds (`setConnectTimeout(Duration.ofSeconds(3))`).
  - Read timeout: 5 seconds (`setReadTimeout(Duration.ofSeconds(5))`).
- **Resilience & Error Mapping:**
  - Downstream `422 Unprocessable Entity` $\rightarrow$ Translated to Spring `400 Bad Request` with FastAPI's exact validation message.
  - Connection refused / timeout / `503 Service Unavailable` from FastAPI $\rightarrow$ Translated to clean HTTP `503 Service Unavailable` with message: *"Inference service is currently unavailable. Predictions cannot be computed at this time."*
  - No internal python stack traces, file paths, or sockets exposed to client.

---

## 8. Environment Variables & Configuration Plan

All configurations are driven by environment variables with fallback defaults for local Windows execution without Docker:

| Environment Variable | Property Name | Default Value | Description |
|---|---|---|---|
| `SERVER_PORT` | `server.port` | `8080` | Port for Spring Boot backend |
| `SPRING_DATASOURCE_URL` | `spring.datasource.url` | `jdbc:postgresql://localhost:5432/propvalueai_db` | PostgreSQL JDBC connection URL |
| `SPRING_DATASOURCE_USERNAME` | `spring.datasource.username` | `postgres` | Database username |
| `SPRING_DATASOURCE_PASSWORD` | `spring.datasource.password` | `postgres` | Database password |
| `JWT_SECRET` | `propvalueai.jwt.secret` | *(64-char hex key for local dev)* | HMAC-SHA256 signature key |
| `JWT_EXPIRATION_MS` | `propvalueai.jwt.expiration-ms` | `86400000` (24h) | JWT validity duration |
| `FASTAPI_INFERENCE_URL` | `propvalueai.ml.inference-url` | `http://127.0.0.1:8000` | Internal FastAPI service URL |

---

## 9. Step-by-Step Implementation Order

### Step 1: Maven Project Foundation
- Generate standard `backend/pom.xml` with verified dependencies and Java 21 compilation targets.
- Set up Maven wrapper (`mvnw.cmd`, `.mvn/wrapper/`).
- Create `BackendApplication.java` and `application.yml`.
- Verify build with `mvn clean compile`.

### Step 2: PostgreSQL Persistence & Flyway Migrations
- Set up `db/migration/V1__init_schema.sql` with `users` and `prediction_records`.
- Implement `UserEntity`, `PredictionRecordEntity`, and `Role` enum.
- Implement `UserRepository` and `PredictionRecordRepository`.
- Write `@DataJpaTest` to verify schema generation and repository queries.

### Step 3: Security, JWT, and Authentication
- Implement `JwtTokenProvider`, `JwtAuthenticationFilter`, `SecurityUserPrincipal`, and `CustomUserDetailsService`.
- Configure `SecurityConfig` with BCrypt and stateless security filter chain.
- Implement `AuthController`, `AuthService`, and validation DTOs.
- Write unit tests for JWT and `@WebMvcTest` for registration/login endpoints.

### Step 4: FastAPI Client & Resilient Service Layer
- Implement `RestClientConfig` and `FastApiClientService`.
- Map incoming DTOs to FastAPI requests, handling conversions and timeouts safely.
- Write tests with `MockRestServiceServer` simulating successful responses, timeouts, 422 errors, and 503 unavailable states.

### Step 5: Prediction Orchestration & History Management
- Implement `PredictionController` and `PredictionService`:
  - Validates property inputs.
  - Queries `FastApiClientService`.
  - Persists record with `user_id` in `prediction_records`.
  - Returns `PredictionResponse` carrying the mandatory disclaimer.
- Implement user-isolated history (`GET /api/v1/predictions`) and admin history (`GET /api/v1/admin/predictions`).
- Implement `GlobalExceptionHandler` for centralized, secure error handling.

### Step 6: OpenAPI Documentation & Verification Suite
- Configure `OpenApiConfig` with JWT Bearer scheme and documented schemas.
- Implement `/api/v1/health` endpoint checking DB and FastAPI readiness.
- Execute full test suite (`mvn clean test`).
- Document manual verification steps in `backend/README.md`.

---

## 10. Risks, Assumptions & Decisions for Review

1. **Local Database Instance:**
   - *Assumption:* A local PostgreSQL instance is running on port 5432. The database `propvalueai_db` must be created by the user or initial setup script.
2. **Anonymous vs Authenticated Predictions:**
   - *Design Decision:* Both options can be supported cleanly:
     - If authenticated, the user ID is attached to the record and appears in `/api/v1/predictions` history.
     - If unauthenticated, the prediction succeeds with `user_id = NULL` (enabling guest property estimates without forcing login), but history tracking requires an account.
3. **Mandatory Educational Disclaimer:**
   - Verified that the exact disclaimer string:
     `"PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."`
     will be embedded in every single prediction response and persisted in the database record.

---
**Status:** Audit and implementation plan complete. Ready for project owner review. Application code implementation will begin immediately upon approval.

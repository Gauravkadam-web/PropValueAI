# PropValueAI — Spring Boot Backend Service (Phase 4)

## Overview
The PropValueAI backend is a robust, production-grade Spring Boot service managing authentication, authorization, property price prediction persistence, audit history, and internal communication with the Python FastAPI ML inference service.

Built according to the approved architecture in `docs/architecture.md`, `docs/api-contracts.md`, and `prompts/phase4.md`.

---

## 1. Prerequisites & Environment
- **Java:** `Java 21 LTS` (Verified: `Java 21.0.8 LTS` / `25.0.1 LTS`)
- **Maven:** `Apache Maven 3.9+`
- **Database:** `PostgreSQL 15+` (Local service on port `5432`)
- **Python / ML Service:** `Python 3.12+` with virtual environment (`.venv`) for FastAPI inference.
- **Operating System:** Windows PowerShell or Linux/macOS bash.

---

## 2. PostgreSQL Database Setup
Create the application database using PostgreSQL CLI (`psql`) or pgAdmin:

```sql
CREATE DATABASE propvalueai_db;
```

Schema tables and indexes are automatically created and managed on backend startup via **Flyway** migrations located in:
`backend/src/main/resources/db/migration/V1__init_schema.sql`

Managed tables:
- `users`: User profiles, BCrypt hashed passwords, role assignment (`ROLE_USER`, `ROLE_ADMIN`).
- `prediction_records`: Historical property predictions with input parameters, predicted price, target unit, model metadata, and educational disclaimer.

---

## 3. Environment Variable Configuration
The AI agent never accesses or creates real `.env` files. Configure your environment using the template provided in `backend/.env.example`.

### PowerShell Setup Example (Windows)
```powershell
# Database
$env:SPRING_DATASOURCE_URL="jdbc:postgresql://localhost:5432/propvalueai_db"
$env:SPRING_DATASOURCE_USERNAME="postgres"
$env:SPRING_DATASOURCE_PASSWORD="your_local_postgres_password"

# JWT Authentication (Key must be at least 256 bits / 32 characters)
$env:PROPVALUEAI_JWT_SECRET="your_secure_sample_jwt_secret_key_min_32_characters_123456"
$env:PROPVALUEAI_JWT_EXPIRATION="86400000"

# FastAPI ML Inference Service URL
$env:PROPVALUEAI_FASTAPI_BASE_URL="http://127.0.0.1:8000"

# Secure Initial Administrator Provisioning (Optional)
$env:PROPVALUEAI_ADMIN_EMAIL="admin@propvalueai.local"
$env:PROPVALUEAI_ADMIN_PASSWORD="AdminSecurePassword123!"
$env:PROPVALUEAI_ADMIN_FIRST_NAME="System"
$env:PROPVALUEAI_ADMIN_LAST_NAME="Administrator"

# CORS Configuration
$env:PROPVALUEAI_CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

---

## 4. Secure Administrator Provisioning
- **Public Registration Isolation:** Public registration (`POST /api/v1/auth/register`) strictly assigns `ROLE_USER`. Callers cannot register as administrators.
- **Zero Hardcoded Credentials:** No default admin credentials exist in code or migrations.
- **Environment-Driven Initialization:** An administrator account is provisioned on initial startup only when `PROPVALUEAI_ADMIN_EMAIL` and `PROPVALUEAI_ADMIN_PASSWORD` are provided in the environment. If the account already exists, existing credentials and records are preserved.

---

## 5. Starting the Services

### Step 5.1: Start the Python FastAPI ML Service
In the project root directory:
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run FastAPI server
uvicorn ml.inference.api.app:app --host 127.0.0.1 --port 8000
```
Verify readiness:
`http://127.0.0.1:8000/health/ready` (Returns `200 OK`)

### Step 5.2: Start the Spring Boot Backend
In the `backend/` directory:
```powershell
mvn spring-boot:run
```
The server will start on port `8080` (or `SERVER_PORT`).

---

## 6. OpenAPI / Swagger Documentation
Interactive API documentation and schema explorer:
- **Swagger UI:** [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html)
- **OpenAPI 3 JSON Spec:** [http://localhost:8080/v3/api-docs](http://localhost:8080/v3/api-docs)

To test authenticated endpoints in Swagger UI, click **Authorize** and supply:
`Bearer <your_jwt_token>`

---

## 7. End-to-End API Usage Flow

### 7.1 Register a New Account
```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "UserSecurePass123!",
    "first_name": "Gaurav",
    "last_name": "Kadam"
  }'
```

### 7.2 Log In to Obtain JWT Token
```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "UserSecurePass123!"
  }'
```
Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "type": "Bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Gaurav",
    "last_name": "Kadam",
    "role": "ROLE_USER",
    "created_at": "2026-10-22T10:00:00Z"
  }
}
```

### 7.3 Submit Property for Prediction (Authenticated)
> **Note:** Every prediction strictly requires an authenticated user. Guest predictions are rejected with `401 Unauthorized`.
```bash
curl -X POST http://localhost:8080/api/v1/predictions \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "total_sqft": 1056.0,
    "size": "2 BHK",
    "bath": 2.0,
    "balcony": 1.0,
    "area_type": "Super built-up  Area"
  }'
```
Response:
```json
{
  "id": 1,
  "predicted_price": 55.20,
  "target_unit": "Lakhs INR",
  "model_name": "Random Forest",
  "model_version": "1.0.0",
  "fastapi_prediction_id": "98173fc5-ffeb-4373-8167-8e9d29d9ccaf",
  "disclaimer": "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.",
  "created_at": "2026-10-22T10:05:00Z"
}
```

### 7.4 Fetch User Prediction History
```bash
curl -X GET "http://localhost:8080/api/v1/predictions?page=0&size=10" \
  -H "Authorization: Bearer <your_jwt_token>"
```

### 7.5 Health Check
```bash
curl -X GET http://localhost:8080/api/v1/health
```
Response:
```json
{
  "timestamp": "2026-10-22T10:10:00Z",
  "service": "propvalueai-backend",
  "status": "UP",
  "components": {
    "database": {
      "status": "UP",
      "type": "PostgreSQL"
    },
    "inference_service": {
      "status": "UP",
      "ready": true
    }
  }
}
```

---

## 8. Automated Testing
Run the complete backend test suite:
```powershell
cd backend
mvn test
```
Test categories executed:
- `JwtTokenProviderTest`: Token generation, claim decoding, expiration, signature verification.
- `UserRepositoryTest`: Data JPA persistence, constraints, case-normalized lookup.
- `AuthControllerTest`: Registration validation, duplicate email conflict (409), password length validation, authentication (200/401).
- `PredictionControllerTest`: Guest rejection (401), authenticated prediction & persistence, user history isolation, admin-only endpoint protection (403/200).
- `FastApiClientServiceTest`: RestClient integration with MockRestServiceServer handling 200 OK, 422 validation, 503 unavailable, and health probe.
- `BackendApplicationTests`: ApplicationContext smoke test.

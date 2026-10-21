# API Contracts — Preliminary

**Status:** Draft only. Final schemas depend on dataset inspection, model design, and approved application requirements.

## 1. Service boundaries

### Browser → Spring Boot
The Next.js browser client communicates with Spring Boot application APIs. It must not access PostgreSQL directly or call the internal FastAPI service directly.

### Spring Boot → FastAPI
Spring Boot calls the internal inference service using a server-to-server request. The request must match the feature contract established by the verified training dataset.

### Spring Boot → PostgreSQL
Spring Boot owns application database access, migrations, and persistence for users, roles, prediction records, and related metadata.

## 2. Candidate FastAPI endpoints

These paths are proposed and must be confirmed during implementation.

| Method | Path | Purpose | Status |
|---|---|---|---|
| GET | `/api/v1/health` | Check service health | Proposed |
| GET | `/api/v1/model-info` | Return safe model/version metadata | Proposed |
| POST | `/api/v1/predict` | Predict from validated property features | Proposed |

## 3. Prediction contract — pending decisions

Do not hardcode example features as the final contract. Before finalizing the schema, inspect the dataset and approve:
- exact feature names and types
- target-price definition and currency
- area units
- accepted location representation and unseen-location behavior
- property type and other supported inputs
- valid ranges and missing-value behavior
- model version and response metadata requirements

The eventual response should include a numeric estimated price and appropriate model/version metadata, subject to the approved design. It must not imply guaranteed valuation or unsupported confidence intervals.

## 4. Error behavior

Define consistent error codes and schemas during implementation for:
- invalid or missing input
- unsupported category/location
- model artifact unavailable or incompatible
- inference service unavailable or timed out
- prediction failure
- persistence failure in the application backend

Never return stack traces, secrets, or internal paths to users.

## 5. Authentication and authorization

- Authentication and application authorization belong to Spring Boot.
- FastAPI is an internal inference service and should not expose a public browser-facing prediction API.
- Admin endpoints must enforce server-side role checks.
- Final token/session approach and endpoint paths remain to be approved.

## 6. Contract change protocol

When the dataset or model feature schema changes:
1. Update the ML training contract.
2. Update FastAPI request validation.
3. Update Spring Boot DTOs and integration tests.
4. Update frontend form validation and UI.
5. Update this document and test the complete flow.

# Real Estate Price Prediction Using Python and Machine Learning

**Project status:** Planning / Phase 0  
**Purpose:** Estimate residential property prices from verified historical property data using a trained machine-learning model.

## Overview

This repository will contain a web application with three application components:

- **Frontend:** Next.js, TypeScript, and Tailwind CSS
- **Application backend:** Java 21 and Spring Boot
- **ML inference service:** Python and FastAPI
- **Database:** PostgreSQL, managed by Spring Boot
- **Database migrations:** Flyway
- **ML stack:** pandas, NumPy, scikit-learn, and joblib

The application will accept property details, request an estimate from the Python inference service through Spring Boot, store prediction history in PostgreSQL, and display the result in the frontend.

## Architecture principles

1. Model training is an offline workflow; a user prediction request must not retrain the model.
2. The saved ML artifact contains the fitted preprocessing pipeline and estimator.
3. Training and inference must use compatible, tested dependency versions.
4. Spring Boot is the primary owner of application database access.
5. The browser communicates with Spring Boot, not directly with PostgreSQL or the internal ML service.
6. Dataset columns, target price, currency, area units, supported locations, and property types must be confirmed by inspecting the actual dataset.
7. A prediction is an estimate, not a guaranteed market valuation.

## Planned features

### User module
- Account registration and login
- Property details form
- Estimated price result
- Prediction history
- User profile management

### Admin module
- Dashboard and system statistics
- User management
- Prediction history oversight
- Reports and analytics
- Role-based access control
- Admin profile management

These are planned features, not implemented functionality.

## Repository structure

```text
PropValueAI/
├── AGENTS.md
├── README.md
├── .gitignore
├── frontend/
├── backend/
├── ml/
│   ├── training/
│   │   ├── data/
│   │   │   ├── raw/
│   │   │   ├── processed/
│   │   │   └── external/
│   │   ├── scripts/
│   │   ├── experiments/
│   │   └── requirements.txt
│   ├── inference/
│   │   ├── model/
│   │   ├── preprocessing/
│   │   ├── services/
│   │   ├── artifacts/
│   │   └── config/
│   ├── pipeline/
│   ├── common/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
└── docs/
    ├── architecture.md
    ├── development-roadmap.md
    └── api-contracts.md
```

Optional modules should only be implemented when they provide real value. Preserve this agreed structure unless a change is explained and approved.

## Dataset status

Two candidates have been discussed:
1. Pune House Price dataset: https://github.com/Sahil9822/Pune-House-Price-Prediction
2. Indian Urban House Price Prediction: https://www.kaggle.com/competitions/indian-urban-house-price-prediction/data

A possible CSV URL discussed for the Pune data is:
https://raw.githubusercontent.com/prashantmane92/dataset/main/Pune_House_Data.csv

These are **unverified candidates**, not yet approved training inputs. Inspect the actual files, columns, provenance, license, target-price meaning, currency, units, missing values, duplicates, and geographic coverage before choosing or combining datasets. Do not assume compatibility.

## Development phases

- Phase 0: Repository foundation and project documentation
- Phase 1: Dataset inspection and validation
- Phase 2: EDA, preprocessing, training, model comparison, and evaluation
- Phase 3: FastAPI inference service and model loading
- Phase 4: Spring Boot backend, database schema, Flyway, and ML-service integration
- Phase 5: Next.js frontend
- Phase 6: End-to-end integration, security, and testing
- Phase 7: Production preparation and deployment

## Current status

Phase 0, Phase 1, Phase 2, and Phase 3 are complete. The Python FastAPI ML inference service is fully functional and ready to be queried by the Spring Boot backend in Phase 4. For fresh-clone setup instructions (running existing model vs regenerating artifacts), see [`ml/README.md`](ml/README.md).

## Security and repository hygiene

- Never commit secrets, credentials, local environment files, private datasets, or untrusted model artifacts.
- Use environment-driven configuration for future services.
- Do not load joblib/pickle artifacts from untrusted sources.
- Do not fabricate model metrics or represent synthetic data as real market data.
- Review dataset licensing and repository size before committing data.

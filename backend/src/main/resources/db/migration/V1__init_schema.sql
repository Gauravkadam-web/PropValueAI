-- ==============================================================================
-- Flyway Database Migration: V1__init_schema.sql
-- PropValueAI Core Application Schema: Users and Prediction History
-- ==============================================================================

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

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS prediction_records (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
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

CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON prediction_records(user_id);
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON prediction_records(created_at DESC);

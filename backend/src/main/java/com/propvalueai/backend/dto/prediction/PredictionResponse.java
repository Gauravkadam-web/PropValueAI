package com.propvalueai.backend.dto.prediction;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

public class PredictionResponse {

    private Long id;

    @JsonProperty("predicted_price")
    private BigDecimal predictedPrice;

    @JsonProperty("target_unit")
    private String targetUnit = "Lakhs INR";

    @JsonProperty("model_name")
    private String modelName;

    @JsonProperty("model_version")
    private String modelVersion;

    @JsonProperty("fastapi_prediction_id")
    private String fastapiPredictionId;

    private String disclaimer;

    @JsonProperty("created_at")
    private OffsetDateTime createdAt;

    public PredictionResponse() {
    }

    public PredictionResponse(Long id, BigDecimal predictedPrice, String targetUnit, String modelName,
                              String modelVersion, String fastapiPredictionId, String disclaimer, OffsetDateTime createdAt) {
        this.id = id;
        this.predictedPrice = predictedPrice;
        this.targetUnit = targetUnit;
        this.modelName = modelName;
        this.modelVersion = modelVersion;
        this.fastapiPredictionId = fastapiPredictionId;
        this.disclaimer = disclaimer;
        this.createdAt = createdAt;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public BigDecimal getPredictedPrice() {
        return predictedPrice;
    }

    public void setPredictedPrice(BigDecimal predictedPrice) {
        this.predictedPrice = predictedPrice;
    }

    public String getTargetUnit() {
        return targetUnit;
    }

    public void setTargetUnit(String targetUnit) {
        this.targetUnit = targetUnit;
    }

    public String getModelName() {
        return modelName;
    }

    public void setModelName(String modelName) {
        this.modelName = modelName;
    }

    public String getModelVersion() {
        return modelVersion;
    }

    public void setModelVersion(String modelVersion) {
        this.modelVersion = modelVersion;
    }

    public String getFastapiPredictionId() {
        return fastapiPredictionId;
    }

    public void setFastapiPredictionId(String fastapiPredictionId) {
        this.fastapiPredictionId = fastapiPredictionId;
    }

    public String getDisclaimer() {
        return disclaimer;
    }

    public void setDisclaimer(String disclaimer) {
        this.disclaimer = disclaimer;
    }

    public OffsetDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(OffsetDateTime createdAt) {
        this.createdAt = createdAt;
    }
}

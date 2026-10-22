package com.propvalueai.backend.dto.prediction;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.math.BigDecimal;

public class FastApiPredictResponse {

    @JsonProperty("prediction_id")
    private String predictionId;

    @JsonProperty("predicted_price")
    private BigDecimal predictedPrice;

    @JsonProperty("target_unit")
    private String targetUnit = "Lakhs INR";

    @JsonProperty("model_name")
    private String modelName;

    @JsonProperty("model_version")
    private String modelVersion;

    private String disclaimer;

    public FastApiPredictResponse() {
    }

    public FastApiPredictResponse(String predictionId, BigDecimal predictedPrice, String targetUnit,
                                  String modelName, String modelVersion, String disclaimer) {
        this.predictionId = predictionId;
        this.predictedPrice = predictedPrice;
        this.targetUnit = targetUnit;
        this.modelName = modelName;
        this.modelVersion = modelVersion;
        this.disclaimer = disclaimer;
    }

    public String getPredictionId() {
        return predictionId;
    }

    public void setPredictionId(String predictionId) {
        this.predictionId = predictionId;
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

    public String getDisclaimer() {
        return disclaimer;
    }

    public void setDisclaimer(String disclaimer) {
        this.disclaimer = disclaimer;
    }
}

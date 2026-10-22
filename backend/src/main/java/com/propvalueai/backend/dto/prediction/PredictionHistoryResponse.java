package com.propvalueai.backend.dto.prediction;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.propvalueai.backend.entity.PredictionRecordEntity;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

public class PredictionHistoryResponse {

    private Long id;

    @JsonProperty("total_sqft")
    private String totalSqft;

    private String size;
    private Double bath;
    private Double balcony;

    @JsonProperty("area_type")
    private String areaType;

    @JsonProperty("predicted_price")
    private BigDecimal predictedPrice;

    @JsonProperty("target_unit")
    private String targetUnit;

    @JsonProperty("model_name")
    private String modelName;

    @JsonProperty("model_version")
    private String modelVersion;

    private String status;

    @JsonProperty("created_at")
    private OffsetDateTime createdAt;

    // Populated for admin view
    @JsonProperty("user_email")
    private String userEmail;

    public PredictionHistoryResponse() {
    }

    public static PredictionHistoryResponse fromEntity(PredictionRecordEntity record) {
        PredictionHistoryResponse response = new PredictionHistoryResponse();
        response.setId(record.getId());
        response.setTotalSqft(record.getTotalSqftInput());
        response.setSize(record.getSizeInput());
        response.setBath(record.getBathInput());
        response.setBalcony(record.getBalconyInput());
        response.setAreaType(record.getAreaTypeInput());
        response.setPredictedPrice(record.getPredictedPriceLakhs());
        response.setTargetUnit(record.getTargetUnit());
        response.setModelName(record.getModelName());
        response.setModelVersion(record.getModelVersion());
        response.setStatus(record.getStatus());
        response.setCreatedAt(record.getCreatedAt());
        if (record.getUser() != null) {
            response.setUserEmail(record.getUser().getEmail());
        }
        return response;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTotalSqft() {
        return totalSqft;
    }

    public void setTotalSqft(String totalSqft) {
        this.totalSqft = totalSqft;
    }

    public String getSize() {
        return size;
    }

    public void setSize(String size) {
        this.size = size;
    }

    public Double getBath() {
        return bath;
    }

    public void setBath(Double bath) {
        this.bath = bath;
    }

    public Double getBalcony() {
        return balcony;
    }

    public void setBalcony(Double balcony) {
        this.balcony = balcony;
    }

    public String getAreaType() {
        return areaType;
    }

    public void setAreaType(String areaType) {
        this.areaType = areaType;
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

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public OffsetDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(OffsetDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public String getUserEmail() {
        return userEmail;
    }

    public void setUserEmail(String userEmail) {
        this.userEmail = userEmail;
    }
}

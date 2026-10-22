package com.propvalueai.backend.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.Objects;

@Entity
@Table(name = "prediction_records")
public class PredictionRecordEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false)
    private UserEntity user;

    @Column(name = "total_sqft_input", nullable = false, length = 100)
    private String totalSqftInput;

    @Column(name = "size_input", length = 50)
    private String sizeInput;

    @Column(name = "bath_input")
    private Double bathInput;

    @Column(name = "balcony_input")
    private Double balconyInput;

    @Column(name = "area_type_input", length = 100)
    private String areaTypeInput;

    @Column(name = "predicted_price_lakhs", nullable = false, precision = 12, scale = 2)
    private BigDecimal predictedPriceLakhs;

    @Column(name = "target_unit", nullable = false, length = 50)
    private String targetUnit = "Lakhs INR";

    @Column(name = "model_name", nullable = false, length = 100)
    private String modelName;

    @Column(name = "model_version", nullable = false, length = 50)
    private String modelVersion;

    @Column(name = "fastapi_prediction_id", length = 100)
    private String fastapiPredictionId;

    @Column(name = "disclaimer", nullable = false, columnDefinition = "TEXT")
    private String disclaimer;

    @Column(name = "status", nullable = false, length = 50)
    private String status = "SUCCESS";

    @Column(name = "created_at", nullable = false, updatable = false)
    private OffsetDateTime createdAt;

    public PredictionRecordEntity() {
    }

    @PrePersist
    protected void onCreate() {
        if (this.createdAt == null) {
            this.createdAt = OffsetDateTime.now();
        }
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public UserEntity getUser() {
        return user;
    }

    public void setUser(UserEntity user) {
        this.user = user;
    }

    public String getTotalSqftInput() {
        return totalSqftInput;
    }

    public void setTotalSqftInput(String totalSqftInput) {
        this.totalSqftInput = totalSqftInput;
    }

    public String getSizeInput() {
        return sizeInput;
    }

    public void setSizeInput(String sizeInput) {
        this.sizeInput = sizeInput;
    }

    public Double getBathInput() {
        return bathInput;
    }

    public void setBathInput(Double bathInput) {
        this.bathInput = bathInput;
    }

    public Double getBalconyInput() {
        return balconyInput;
    }

    public void setBalconyInput(Double balconyInput) {
        this.balconyInput = balconyInput;
    }

    public String getAreaTypeInput() {
        return areaTypeInput;
    }

    public void setAreaTypeInput(String areaTypeInput) {
        this.areaTypeInput = areaTypeInput;
    }

    public BigDecimal getPredictedPriceLakhs() {
        return predictedPriceLakhs;
    }

    public void setPredictedPriceLakhs(BigDecimal predictedPriceLakhs) {
        this.predictedPriceLakhs = predictedPriceLakhs;
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

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PredictionRecordEntity that = (PredictionRecordEntity) o;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}

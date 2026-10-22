package com.propvalueai.backend.dto.prediction;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;

public class PropertyInputRequest {

    @NotNull(message = "total_sqft is required.")
    @JsonProperty("total_sqft")
    private Object totalSqft;

    @JsonProperty("size")
    private Object size;

    @DecimalMin(value = "0.0", message = "bath must be greater than or equal to 0.")
    @DecimalMax(value = "20.0", message = "bath must be less than or equal to 20.")
    @JsonProperty("bath")
    private Double bath;

    @DecimalMin(value = "0.0", message = "balcony must be greater than or equal to 0.")
    @DecimalMax(value = "10.0", message = "balcony must be less than or equal to 10.")
    @JsonProperty("balcony")
    private Double balcony;

    @JsonProperty("area_type")
    private String areaType;

    // Reject target leakage
    @JsonProperty("price")
    private Object price;

    public PropertyInputRequest() {
    }

    public PropertyInputRequest(Object totalSqft, Object size, Double bath, Double balcony, String areaType) {
        this.totalSqft = totalSqft;
        this.size = size;
        this.bath = bath;
        this.balcony = balcony;
        this.areaType = areaType;
    }

    public Object getTotalSqft() {
        return totalSqft;
    }

    public void setTotalSqft(Object totalSqft) {
        this.totalSqft = totalSqft;
    }

    public Object getSize() {
        return size;
    }

    public void setSize(Object size) {
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

    public Object getPrice() {
        return price;
    }

    public void setPrice(Object price) {
        this.price = price;
    }

    public String getTotalSqftAsString() {
        return totalSqft != null ? String.valueOf(totalSqft).trim() : null;
    }

    public String getSizeAsString() {
        return size != null ? String.valueOf(size).trim() : null;
    }
}

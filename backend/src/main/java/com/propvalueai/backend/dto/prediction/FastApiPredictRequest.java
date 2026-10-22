package com.propvalueai.backend.dto.prediction;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class FastApiPredictRequest {

    @JsonProperty("total_sqft")
    private Object totalSqft;

    @JsonProperty("size")
    private Object size;

    @JsonProperty("bath")
    private Double bath;

    @JsonProperty("balcony")
    private Double balcony;

    @JsonProperty("area_type")
    private String areaType;

    public FastApiPredictRequest() {
    }

    public FastApiPredictRequest(Object totalSqft, Object size, Double bath, Double balcony, String areaType) {
        this.totalSqft = totalSqft;
        this.size = size;
        this.bath = bath;
        this.balcony = balcony;
        this.areaType = areaType;
    }

    public static FastApiPredictRequest fromPropertyInput(PropertyInputRequest request) {
        return new FastApiPredictRequest(
                request.getTotalSqft(),
                request.getSize(),
                request.getBath(),
                request.getBalcony(),
                request.getAreaType()
        );
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
}

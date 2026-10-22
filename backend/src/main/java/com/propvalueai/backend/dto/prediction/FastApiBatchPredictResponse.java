package com.propvalueai.backend.dto.prediction;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class FastApiBatchPredictResponse {

    private List<FastApiPredictResponse> predictions;
    private int count;

    @JsonProperty("model_name")
    private String modelName;

    @JsonProperty("model_version")
    private String modelVersion;

    private String disclaimer;

    public FastApiBatchPredictResponse() {
    }

    public List<FastApiPredictResponse> getPredictions() {
        return predictions;
    }

    public void setPredictions(List<FastApiPredictResponse> predictions) {
        this.predictions = predictions;
    }

    public int getCount() {
        return count;
    }

    public void setCount(int count) {
        this.count = count;
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

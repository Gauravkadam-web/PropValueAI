package com.propvalueai.backend.dto.prediction;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

import java.util.List;

public class BatchPropertyInputRequest {

    @NotEmpty(message = "Properties list must not be empty.")
    @Size(min = 1, max = 100, message = "Batch size must be between 1 and 100 properties.")
    @Valid
    private List<PropertyInputRequest> properties;

    public BatchPropertyInputRequest() {
    }

    public BatchPropertyInputRequest(List<PropertyInputRequest> properties) {
        this.properties = properties;
    }

    public List<PropertyInputRequest> getProperties() {
        return properties;
    }

    public void setProperties(List<PropertyInputRequest> properties) {
        this.properties = properties;
    }
}

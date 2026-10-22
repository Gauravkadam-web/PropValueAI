package com.propvalueai.backend.exception;

import org.springframework.http.HttpStatus;

public class InferenceServiceException extends RuntimeException {

    private final HttpStatus status;

    public InferenceServiceException(String message) {
        super(message);
        this.status = HttpStatus.SERVICE_UNAVAILABLE;
    }

    public InferenceServiceException(String message, HttpStatus status) {
        super(message);
        this.status = status;
    }

    public HttpStatus getStatus() {
        return status;
    }
}

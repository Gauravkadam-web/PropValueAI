package com.propvalueai.backend.service;

import com.propvalueai.backend.dto.prediction.FastApiBatchPredictResponse;
import com.propvalueai.backend.dto.prediction.FastApiPredictRequest;
import com.propvalueai.backend.dto.prediction.FastApiPredictResponse;
import com.propvalueai.backend.exception.InferenceServiceException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClient;

import java.util.List;
import java.util.Map;

@Service
public class FastApiClientService {

    private static final Logger log = LoggerFactory.getLogger(FastApiClientService.class);

    private final RestClient restClient;

    public FastApiClientService(RestClient fastApiRestClient) {
        this.restClient = fastApiRestClient;
    }

    public FastApiPredictResponse predict(FastApiPredictRequest request) {
        try {
            return restClient.post()
                    .uri("/api/v1/predict")
                    .contentType(MediaType.APPLICATION_JSON)
                    .accept(MediaType.APPLICATION_JSON)
                    .body(request)
                    .retrieve()
                    .onStatus(HttpStatusCode::is4xxClientError, (req, resp) -> {
                        String body = new String(resp.getBody().readAllBytes());
                        log.warn("FastAPI 4xx client error: status={}, body={}", resp.getStatusCode(), body);
                        if (resp.getStatusCode().value() == 422) {
                            throw new InferenceServiceException("Validation error from inference service: " + extractMessage(body), HttpStatus.BAD_REQUEST);
                        }
                        throw new InferenceServiceException("Inference service rejected request: " + extractMessage(body), HttpStatus.BAD_REQUEST);
                    })
                    .onStatus(HttpStatusCode::is5xxServerError, (req, resp) -> {
                        String body = new String(resp.getBody().readAllBytes());
                        log.error("FastAPI 5xx server error: status={}, body={}", resp.getStatusCode(), body);
                        if (resp.getStatusCode().value() == 503) {
                            throw new InferenceServiceException("Inference service is currently not ready to handle prediction requests.", HttpStatus.SERVICE_UNAVAILABLE);
                        }
                        throw new InferenceServiceException("Inference computation failed in downstream engine.", HttpStatus.SERVICE_UNAVAILABLE);
                    })
                    .body(FastApiPredictResponse.class);
        } catch (ResourceAccessException ex) {
            log.error("Unable to connect to FastAPI inference engine: {}", ex.getMessage());
            throw new InferenceServiceException("Inference service is currently unavailable. Please verify the Python FastAPI engine is running.", HttpStatus.SERVICE_UNAVAILABLE);
        } catch (InferenceServiceException ex) {
            throw ex;
        } catch (Exception ex) {
            log.error("Unexpected error communicating with inference engine", ex);
            throw new InferenceServiceException("Unexpected failure during ML inference call.", HttpStatus.SERVICE_UNAVAILABLE);
        }
    }

    public FastApiBatchPredictResponse predictBatch(List<FastApiPredictRequest> properties) {
        try {
            Map<String, Object> payload = Map.of("properties", properties);
            return restClient.post()
                    .uri("/api/v1/predict/batch")
                    .contentType(MediaType.APPLICATION_JSON)
                    .accept(MediaType.APPLICATION_JSON)
                    .body(payload)
                    .retrieve()
                    .onStatus(HttpStatusCode::is4xxClientError, (req, resp) -> {
                        String body = new String(resp.getBody().readAllBytes());
                        log.warn("FastAPI batch 4xx error: status={}, body={}", resp.getStatusCode(), body);
                        throw new InferenceServiceException("Inference service rejected batch: " + extractMessage(body), HttpStatus.BAD_REQUEST);
                    })
                    .onStatus(HttpStatusCode::is5xxServerError, (req, resp) -> {
                        String body = new String(resp.getBody().readAllBytes());
                        log.error("FastAPI batch 5xx error: status={}, body={}", resp.getStatusCode(), body);
                        throw new InferenceServiceException("Inference service is unavailable.", HttpStatus.SERVICE_UNAVAILABLE);
                    })
                    .body(FastApiBatchPredictResponse.class);
        } catch (ResourceAccessException ex) {
            log.error("Unable to connect to FastAPI inference engine for batch: {}", ex.getMessage());
            throw new InferenceServiceException("Inference service is currently unavailable. Please verify the Python FastAPI engine is running.", HttpStatus.SERVICE_UNAVAILABLE);
        } catch (InferenceServiceException ex) {
            throw ex;
        } catch (Exception ex) {
            log.error("Unexpected error communicating with inference engine for batch", ex);
            throw new InferenceServiceException("Unexpected failure during batch ML inference.", HttpStatus.SERVICE_UNAVAILABLE);
        }
    }

    public boolean isReady() {
        try {
            return restClient.get()
                    .uri("/health/ready")
                    .retrieve()
                    .toBodilessEntity()
                    .getStatusCode()
                    .is2xxSuccessful();
        } catch (Exception ex) {
            log.warn("FastAPI readiness check failed: {}", ex.getMessage());
            return false;
        }
    }

    private String extractMessage(String body) {
        if (body == null || body.isBlank()) {
            return "No details provided";
        }
        // Return truncated body to prevent overwhelming responses
        if (body.length() > 300) {
            return body.substring(0, 300) + "...";
        }
        return body;
    }
}

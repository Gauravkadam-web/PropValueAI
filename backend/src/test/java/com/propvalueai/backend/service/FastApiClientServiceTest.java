package com.propvalueai.backend.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.propvalueai.backend.dto.prediction.FastApiPredictRequest;
import com.propvalueai.backend.dto.prediction.FastApiPredictResponse;
import com.propvalueai.backend.exception.InferenceServiceException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestClient;

import java.math.BigDecimal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.*;
import static org.springframework.test.web.client.response.MockRestResponseCreators.*;

class FastApiClientServiceTest {

    private MockRestServiceServer mockServer;
    private FastApiClientService fastApiClientService;
    private ObjectMapper objectMapper;

    @BeforeEach
    void setUp() {
        RestClient.Builder builder = RestClient.builder().baseUrl("http://localhost:8000");
        mockServer = MockRestServiceServer.bindTo(builder).build();
        RestClient restClient = builder.build();
        fastApiClientService = new FastApiClientService(restClient);
        objectMapper = new ObjectMapper();
    }

    @Test
    void shouldReturnPredictionSuccessfullyOn200() throws Exception {
        FastApiPredictResponse expected = new FastApiPredictResponse(
                "pred-1234",
                new BigDecimal("65.50"),
                "Lakhs INR",
                "Random Forest",
                "1.0.0",
                "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."
        );

        mockServer.expect(requestTo("http://localhost:8000/api/v1/predict"))
                .andExpect(method(HttpMethod.POST))
                .andRespond(withSuccess(objectMapper.writeValueAsString(expected), MediaType.APPLICATION_JSON));

        FastApiPredictRequest request = new FastApiPredictRequest(1200.0, "2 BHK", 2.0, 1.0, "Super built-up  Area");
        FastApiPredictResponse response = fastApiClientService.predict(request);

        assertThat(response).isNotNull();
        assertThat(response.getPredictionId()).isEqualTo("pred-1234");
        assertThat(response.getPredictedPrice()).isEqualTo(new BigDecimal("65.50"));
        assertThat(response.getTargetUnit()).isEqualTo("Lakhs INR");
        mockServer.verify();
    }

    @Test
    void shouldThrowInferenceServiceExceptionWhenFastApiReturns503() {
        mockServer.expect(requestTo("http://localhost:8000/api/v1/predict"))
                .andExpect(method(HttpMethod.POST))
                .andRespond(withStatus(HttpStatus.SERVICE_UNAVAILABLE).body("{\"error\": \"Model unready\"}"));

        FastApiPredictRequest request = new FastApiPredictRequest(1200.0, "2 BHK", 2.0, 1.0, "Plot Area");

        assertThatThrownBy(() -> fastApiClientService.predict(request))
                .isInstanceOf(InferenceServiceException.class)
                .hasMessageContaining("not ready");

        mockServer.verify();
    }

    @Test
    void shouldThrowInferenceServiceExceptionWhenFastApiReturns422() {
        mockServer.expect(requestTo("http://localhost:8000/api/v1/predict"))
                .andExpect(method(HttpMethod.POST))
                .andRespond(withStatus(HttpStatus.UNPROCESSABLE_ENTITY).body("{\"detail\": \"Invalid total_sqft\"}"));

        FastApiPredictRequest request = new FastApiPredictRequest(-100.0, "2 BHK", 2.0, 1.0, "Plot Area");

        assertThatThrownBy(() -> fastApiClientService.predict(request))
                .isInstanceOf(InferenceServiceException.class)
                .hasMessageContaining("Validation error");

        mockServer.verify();
    }

    @Test
    void shouldCheckHealthCorrectly() {
        mockServer.expect(requestTo("http://localhost:8000/health/ready"))
                .andExpect(method(HttpMethod.GET))
                .andRespond(withSuccess());

        assertThat(fastApiClientService.isReady()).isTrue();
        mockServer.verify();
    }
}

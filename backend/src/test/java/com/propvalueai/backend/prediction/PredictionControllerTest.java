package com.propvalueai.backend.prediction;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.propvalueai.backend.dto.prediction.FastApiPredictResponse;
import com.propvalueai.backend.dto.prediction.PropertyInputRequest;
import com.propvalueai.backend.entity.PredictionRecordEntity;
import com.propvalueai.backend.entity.Role;
import com.propvalueai.backend.entity.UserEntity;
import com.propvalueai.backend.repository.PredictionRecordRepository;
import com.propvalueai.backend.repository.UserRepository;
import com.propvalueai.backend.security.JwtTokenProvider;
import com.propvalueai.backend.service.FastApiClientService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class PredictionControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PredictionRecordRepository predictionRecordRepository;

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private FastApiClientService fastApiClientService;

    private UserEntity userA;
    private UserEntity userB;
    private UserEntity adminUser;
    private String tokenA;
    private String tokenB;
    private String adminToken;

    @BeforeEach
    void setUp() {
        predictionRecordRepository.deleteAll();
        userRepository.deleteAll();

        userA = userRepository.save(new UserEntity("usera@example.com", passwordEncoder.encode("Password123!"), "User", "A", Role.ROLE_USER));
        userB = userRepository.save(new UserEntity("userb@example.com", passwordEncoder.encode("Password123!"), "User", "B", Role.ROLE_USER));
        adminUser = userRepository.save(new UserEntity("admin@example.com", passwordEncoder.encode("AdminPass123!"), "Admin", "User", Role.ROLE_ADMIN));

        tokenA = jwtTokenProvider.generateToken(userA.getEmail(), userA.getId(), "ROLE_USER", userA.getFirstName(), userA.getLastName());
        tokenB = jwtTokenProvider.generateToken(userB.getEmail(), userB.getId(), "ROLE_USER", userB.getFirstName(), userB.getLastName());
        adminToken = jwtTokenProvider.generateToken(adminUser.getEmail(), adminUser.getId(), "ROLE_ADMIN", adminUser.getFirstName(), adminUser.getLastName());
    }

    @Test
    void shouldRejectGuestPredictionWithUnauthorized() throws Exception {
        PropertyInputRequest request = new PropertyInputRequest(1200.0, "2 BHK", 2.0, 1.0, "Super built-up  Area");

        mockMvc.perform(post("/api/v1/predictions")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.error", is("Unauthorized")));
    }

    @Test
    void shouldAllowAuthenticatedPredictionAndPersistRecord() throws Exception {
        FastApiPredictResponse mockResponse = new FastApiPredictResponse(
                "fastapi-uuid-001",
                new BigDecimal("62.50"),
                "Lakhs INR",
                "Random Forest",
                "1.0.0",
                "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations."
        );
        when(fastApiClientService.predict(any())).thenReturn(mockResponse);

        PropertyInputRequest request = new PropertyInputRequest(1100.0, "2 BHK", 2.0, 1.0, "Super built-up  Area");

        mockMvc.perform(post("/api/v1/predictions")
                        .header("Authorization", "Bearer " + tokenA)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.predicted_price", is(62.50)))
                .andExpect(jsonPath("$.target_unit", is("Lakhs INR")))
                .andExpect(jsonPath("$.model_name", is("Random Forest")))
                .andExpect(jsonPath("$.disclaimer", containsString("PropValueAI provides simulated estimates")));

        // Verify persisted record
        org.assertj.core.api.Assertions.assertThat(predictionRecordRepository.countByUserId(userA.getId())).isEqualTo(1L);
        org.assertj.core.api.Assertions.assertThat(predictionRecordRepository.countByUserId(userB.getId())).isEqualTo(0L);
    }

    @Test
    void shouldEnforceUserIsolationInPredictionHistory() throws Exception {
        // Create 2 records for User A and 1 for User B
        PredictionRecordEntity recA1 = new PredictionRecordEntity();
        recA1.setUser(userA);
        recA1.setTotalSqftInput("1000");
        recA1.setPredictedPriceLakhs(new BigDecimal("50.00"));
        recA1.setModelName("Random Forest");
        recA1.setModelVersion("1.0.0");
        recA1.setDisclaimer("PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.");
        predictionRecordRepository.save(recA1);

        PredictionRecordEntity recB1 = new PredictionRecordEntity();
        recB1.setUser(userB);
        recB1.setTotalSqftInput("1500");
        recB1.setPredictedPriceLakhs(new BigDecimal("75.00"));
        recB1.setModelName("Random Forest");
        recB1.setModelVersion("1.0.0");
        recB1.setDisclaimer("PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.");
        predictionRecordRepository.save(recB1);

        // User A fetches history
        mockMvc.perform(get("/api/v1/predictions")
                        .header("Authorization", "Bearer " + tokenA))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.total_elements", is(1)))
                .andExpect(jsonPath("$.content[0].total_sqft", is("1000")));

        // User B fetches history
        mockMvc.perform(get("/api/v1/predictions")
                        .header("Authorization", "Bearer " + tokenB))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.total_elements", is(1)))
                .andExpect(jsonPath("$.content[0].total_sqft", is("1500")));
    }

    @Test
    void shouldRejectUserAccessToAdminEndpoints() throws Exception {
        mockMvc.perform(get("/api/v1/admin/predictions")
                        .header("Authorization", "Bearer " + tokenA))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.error", is("Forbidden")));
    }

    @Test
    void shouldAllowAdminAccessToAdminEndpoints() throws Exception {
        mockMvc.perform(get("/api/v1/admin/predictions")
                        .header("Authorization", "Bearer " + adminToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.page", is(0)));
    }

    @Test
    void shouldDenyUserAccessToAnotherUsersPredictionById() throws Exception {
        PredictionRecordEntity recB = new PredictionRecordEntity();
        recB.setUser(userB);
        recB.setTotalSqftInput("1800");
        recB.setPredictedPriceLakhs(new BigDecimal("90.00"));
        recB.setModelName("Random Forest");
        recB.setModelVersion("1.0.0");
        recB.setDisclaimer("PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.");
        PredictionRecordEntity savedB = predictionRecordRepository.save(recB);

        // User A attempts to access User B's record
        mockMvc.perform(get("/api/v1/predictions/" + savedB.getId())
                        .header("Authorization", "Bearer " + tokenA))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.error", is("Forbidden")))
                .andExpect(jsonPath("$.status", is(403)));
    }

    @Test
    void shouldAllowUserToAccessTheirOwnPredictionById() throws Exception {
        PredictionRecordEntity recA = new PredictionRecordEntity();
        recA.setUser(userA);
        recA.setTotalSqftInput("1250");
        recA.setPredictedPriceLakhs(new BigDecimal("68.00"));
        recA.setModelName("Random Forest");
        recA.setModelVersion("1.0.0");
        recA.setDisclaimer("PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.");
        PredictionRecordEntity savedA = predictionRecordRepository.save(recA);

        // User A accesses their own record
        mockMvc.perform(get("/api/v1/predictions/" + savedA.getId())
                        .header("Authorization", "Bearer " + tokenA))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(savedA.getId().intValue())))
                .andExpect(jsonPath("$.total_sqft", is("1250")))
                .andExpect(jsonPath("$.predicted_price", is(68.00)));
    }
}

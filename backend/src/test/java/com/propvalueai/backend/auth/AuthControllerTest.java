package com.propvalueai.backend.auth;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.propvalueai.backend.dto.auth.LoginRequest;
import com.propvalueai.backend.dto.auth.RegisterRequest;
import com.propvalueai.backend.entity.Role;
import com.propvalueai.backend.entity.UserEntity;
import com.propvalueai.backend.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.notNullValue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private ObjectMapper objectMapper;

    @BeforeEach
    void cleanUp() {
        userRepository.deleteAll();
    }

    @Test
    void shouldRegisterNewUserSuccessfully() throws Exception {
        RegisterRequest request = new RegisterRequest("john@example.com", "Password123!", "John", "Doe");

        mockMvc.perform(post("/api/v1/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.email", is("john@example.com")))
                .andExpect(jsonPath("$.first_name", is("John")))
                .andExpect(jsonPath("$.last_name", is("Doe")))
                .andExpect(jsonPath("$.role", is("ROLE_USER")));
    }

    @Test
    void shouldRejectDuplicateEmailRegistration() throws Exception {
        UserEntity existing = new UserEntity("existing@example.com", passwordEncoder.encode("Password123!"), "Jane", "Doe", Role.ROLE_USER);
        userRepository.save(existing);

        RegisterRequest duplicateRequest = new RegisterRequest("existing@example.com", "Password123!", "Jane", "Doe");

        mockMvc.perform(post("/api/v1/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(duplicateRequest)))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.error", is("Conflict")));
    }

    @Test
    void shouldRejectRegistrationWithShortPassword() throws Exception {
        RegisterRequest invalid = new RegisterRequest("short@example.com", "short", "Short", "Pass");

        mockMvc.perform(post("/api/v1/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalid)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error", is("Validation Error")));
    }

    @Test
    void shouldLoginSuccessfullyWithValidCredentials() throws Exception {
        UserEntity user = new UserEntity("loginuser@example.com", passwordEncoder.encode("SecretPassword123!"), "Login", "User", Role.ROLE_USER);
        userRepository.save(user);

        LoginRequest request = new LoginRequest("loginuser@example.com", "SecretPassword123!");

        mockMvc.perform(post("/api/v1/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.token", notNullValue()))
                .andExpect(jsonPath("$.type", is("Bearer")))
                .andExpect(jsonPath("$.user.email", is("loginuser@example.com")));
    }

    @Test
    void shouldRejectLoginWithInvalidPassword() throws Exception {
        UserEntity user = new UserEntity("wrongpass@example.com", passwordEncoder.encode("CorrectPassword123!"), "Wrong", "Pass", Role.ROLE_USER);
        userRepository.save(user);

        LoginRequest request = new LoginRequest("wrongpass@example.com", "WrongPassword!");

        mockMvc.perform(post("/api/v1/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.error", is("Unauthorized")));
    }
}

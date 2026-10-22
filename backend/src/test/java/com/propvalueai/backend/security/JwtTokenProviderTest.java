package com.propvalueai.backend.security;

import com.propvalueai.backend.config.AppProperties;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class JwtTokenProviderTest {

    private JwtTokenProvider jwtTokenProvider;

    @BeforeEach
    void setUp() {
        AppProperties appProperties = new AppProperties();
        appProperties.getJwt().setSecret("dGVzdF9zdXBlcl9zZWNyZXRfand0X2tleV9hdF9sZWFzdF8zMl9jaGFycw==");
        appProperties.getJwt().setExpirationMs(3600000L);
        jwtTokenProvider = new JwtTokenProvider(appProperties);
    }

    @Test
    void shouldGenerateAndValidateTokenSuccessfully() {
        String token = jwtTokenProvider.generateToken("user@example.com", 101L, "ROLE_USER", "John", "Doe");

        assertThat(token).isNotBlank();
        assertThat(jwtTokenProvider.validateToken(token)).isTrue();
        assertThat(jwtTokenProvider.getUsernameFromToken(token)).isEqualTo("user@example.com");
        assertThat(jwtTokenProvider.getUserIdFromToken(token)).isEqualTo(101L);
        assertThat(jwtTokenProvider.getRoleFromToken(token)).isEqualTo("ROLE_USER");
    }

    @Test
    void shouldRejectInvalidToken() {
        assertThat(jwtTokenProvider.validateToken("invalid.token.payload")).isFalse();
        assertThat(jwtTokenProvider.validateToken("")).isFalse();
    }

    @Test
    void shouldRejectExpiredToken() {
        AppProperties shortLivedProperties = new AppProperties();
        shortLivedProperties.getJwt().setSecret("dGVzdF9zdXBlcl9zZWNyZXRfand0X2tleV9hdF9sZWFzdF8zMl9jaGFycw==");
        shortLivedProperties.getJwt().setExpirationMs(-1000L); // Expired 1 second ago

        JwtTokenProvider expiredProvider = new JwtTokenProvider(shortLivedProperties);
        String expiredToken = expiredProvider.generateToken("expired@example.com", 1L, "ROLE_USER", "Old", "User");

        assertThat(expiredProvider.validateToken(expiredToken)).isFalse();
    }
}

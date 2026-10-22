package com.propvalueai.backend.security;

import com.propvalueai.backend.config.AppProperties;
import io.jsonwebtoken.*;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import io.jsonwebtoken.security.SignatureException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

@Component
public class JwtTokenProvider {

    private static final Logger log = LoggerFactory.getLogger(JwtTokenProvider.class);

    private final SecretKey key;
    private final long expirationMs;

    public JwtTokenProvider(AppProperties appProperties) {
        String secret = appProperties.getJwt().getSecret();
        this.expirationMs = appProperties.getJwt().getExpirationMs();
        this.key = initializeKey(secret);
    }

    private SecretKey initializeKey(String secret) {
        byte[] keyBytes;
        try {
            // Attempt Base64 decoding first
            keyBytes = Decoders.BASE64.decode(secret);
            if (keyBytes.length < 32) {
                // If decoded key is less than 256 bits, fall back to raw UTF-8 bytes
                keyBytes = secret.getBytes(StandardCharsets.UTF_8);
            }
        } catch (Exception e) {
            keyBytes = secret.getBytes(StandardCharsets.UTF_8);
        }
        return Keys.hmacShaKeyFor(keyBytes);
    }

    public String generateToken(Authentication authentication) {
        SecurityUserPrincipal principal = (SecurityUserPrincipal) authentication.getPrincipal();
        return generateToken(principal.getUsername(), principal.getId(),
                principal.getAuthorities().stream().findFirst().map(a -> a.getAuthority()).orElse("ROLE_USER"),
                principal.getFirstName(), principal.getLastName());
    }

    public String generateToken(String email, Long userId, String role, String firstName, String lastName) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + expirationMs);

        return Jwts.builder()
                .subject(email)
                .claim("userId", userId)
                .claim("role", role)
                .claim("firstName", firstName)
                .claim("lastName", lastName)
                .issuedAt(now)
                .expiration(expiryDate)
                .signWith(key)
                .compact();
    }

    public String getUsernameFromToken(String token) {
        Claims claims = getClaims(token);
        return claims.getSubject();
    }

    public Long getUserIdFromToken(String token) {
        Claims claims = getClaims(token);
        Object userId = claims.get("userId");
        if (userId instanceof Number number) {
            return number.longValue();
        }
        return null;
    }

    public String getRoleFromToken(String token) {
        Claims claims = getClaims(token);
        return claims.get("role", String.class);
    }

    public Claims getClaims(String token) {
        return Jwts.parser()
                .verifyWith(key)
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser().verifyWith(key).build().parseSignedClaims(token);
            return true;
        } catch (SignatureException ex) {
            log.error("Invalid JWT signature");
        } catch (MalformedJwtException ex) {
            log.error("Invalid JWT token format");
        } catch (ExpiredJwtException ex) {
            log.error("Expired JWT token");
        } catch (UnsupportedJwtException ex) {
            log.error("Unsupported JWT token");
        } catch (IllegalArgumentException ex) {
            log.error("JWT claims string is empty or invalid");
        }
        return false;
    }

    public long getExpirationMs() {
        return expirationMs;
    }
}

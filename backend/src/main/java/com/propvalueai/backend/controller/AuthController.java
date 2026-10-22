package com.propvalueai.backend.controller;

import com.propvalueai.backend.dto.auth.AuthResponse;
import com.propvalueai.backend.dto.auth.LoginRequest;
import com.propvalueai.backend.dto.auth.RegisterRequest;
import com.propvalueai.backend.dto.auth.UserProfileResponse;
import com.propvalueai.backend.security.SecurityUserPrincipal;
import com.propvalueai.backend.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/auth")
@Tag(name = "Authentication", description = "User registration, authentication, and profile endpoints")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    @Operation(summary = "Register a new user", description = "Public registration assigns ROLE_USER. Admin registration is prohibited.")
    public ResponseEntity<UserProfileResponse> register(@Valid @RequestBody RegisterRequest request) {
        UserProfileResponse response = authService.register(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PostMapping("/login")
    @Operation(summary = "Authenticate user and issue JWT", description = "Returns a signed Bearer JWT token valid for authorized requests.")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        AuthResponse response = authService.login(request);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/me")
    @SecurityRequirement(name = "Bearer Authentication")
    @Operation(summary = "Get current authenticated user profile", description = "Retrieves profile details for the user associated with the Bearer token.")
    public ResponseEntity<UserProfileResponse> me(@AuthenticationPrincipal SecurityUserPrincipal principal) {
        UserProfileResponse response = authService.getCurrentUserProfile(principal);
        return ResponseEntity.ok(response);
    }
}

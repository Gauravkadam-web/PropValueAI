package com.propvalueai.backend.service;

import com.propvalueai.backend.dto.auth.AuthResponse;
import com.propvalueai.backend.dto.auth.LoginRequest;
import com.propvalueai.backend.dto.auth.RegisterRequest;
import com.propvalueai.backend.dto.auth.UserProfileResponse;
import com.propvalueai.backend.entity.Role;
import com.propvalueai.backend.entity.UserEntity;
import com.propvalueai.backend.exception.DuplicateResourceException;
import com.propvalueai.backend.exception.ResourceNotFoundException;
import com.propvalueai.backend.repository.UserRepository;
import com.propvalueai.backend.security.JwtTokenProvider;
import com.propvalueai.backend.security.SecurityUserPrincipal;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtTokenProvider jwtTokenProvider;

    public AuthService(UserRepository userRepository,
                       PasswordEncoder passwordEncoder,
                       AuthenticationManager authenticationManager,
                       JwtTokenProvider jwtTokenProvider) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.authenticationManager = authenticationManager;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @Transactional
    public UserProfileResponse register(RegisterRequest request) {
        String normalizedEmail = request.getEmail().toLowerCase().trim();

        if (userRepository.existsByEmail(normalizedEmail)) {
            throw new DuplicateResourceException("An account with email " + normalizedEmail + " already exists.");
        }

        UserEntity user = new UserEntity(
                normalizedEmail,
                passwordEncoder.encode(request.getPassword()),
                request.getFirstName().trim(),
                request.getLastName().trim(),
                Role.ROLE_USER // Public registration strictly assigns ROLE_USER
        );

        UserEntity savedUser = userRepository.save(user);
        return UserProfileResponse.fromEntity(savedUser);
    }

    public AuthResponse login(LoginRequest request) {
        String normalizedEmail = request.getEmail().toLowerCase().trim();

        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(normalizedEmail, request.getPassword())
        );

        SecurityUserPrincipal principal = (SecurityUserPrincipal) authentication.getPrincipal();
        String token = jwtTokenProvider.generateToken(authentication);

        UserEntity user = userRepository.findByEmail(principal.getUsername())
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        return new AuthResponse(token, jwtTokenProvider.getExpirationMs() / 1000, UserProfileResponse.fromEntity(user));
    }

    public UserProfileResponse getCurrentUserProfile(SecurityUserPrincipal principal) {
        UserEntity user = userRepository.findById(principal.getId())
                .orElseThrow(() -> new ResourceNotFoundException("User account not found"));
        return UserProfileResponse.fromEntity(user);
    }
}

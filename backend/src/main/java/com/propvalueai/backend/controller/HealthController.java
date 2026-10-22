package com.propvalueai.backend.controller;

import com.propvalueai.backend.repository.UserRepository;
import com.propvalueai.backend.service.FastApiClientService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.OffsetDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/health")
@Tag(name = "Health", description = "System health and dependency probes")
public class HealthController {

    private final UserRepository userRepository;
    private final FastApiClientService fastApiClientService;

    public HealthController(UserRepository userRepository, FastApiClientService fastApiClientService) {
        this.userRepository = userRepository;
        this.fastApiClientService = fastApiClientService;
    }

    @GetMapping
    @Operation(summary = "Health probe", description = "Checks Spring Boot backend liveness, PostgreSQL connectivity, and downstream FastAPI readiness.")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", OffsetDateTime.now());
        response.put("service", "propvalueai-backend");
        response.put("status", "UP");

        Map<String, Object> components = new HashMap<>();

        // Check PostgreSQL
        boolean dbHealthy;
        try {
            userRepository.count();
            dbHealthy = true;
            components.put("database", Map.of("status", "UP", "type", "PostgreSQL"));
        } catch (Exception ex) {
            dbHealthy = false;
            components.put("database", Map.of("status", "DOWN", "error", "Database connection failed"));
        }

        // Check FastAPI Inference Service
        boolean fastApiHealthy = fastApiClientService.isReady();
        components.put("inference_service", Map.of(
                "status", fastApiHealthy ? "UP" : "DOWN",
                "ready", fastApiHealthy
        ));

        response.put("components", components);

        boolean overallHealthy = dbHealthy;
        return ResponseEntity.status(overallHealthy ? HttpStatus.OK : HttpStatus.SERVICE_UNAVAILABLE).body(response);
    }
}

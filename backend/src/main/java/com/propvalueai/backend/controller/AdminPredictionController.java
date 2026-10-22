package com.propvalueai.backend.controller;

import com.propvalueai.backend.dto.common.PageResponse;
import com.propvalueai.backend.dto.prediction.PredictionHistoryResponse;
import com.propvalueai.backend.service.PredictionHistoryService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/admin/predictions")
@PreAuthorize("hasRole('ADMIN')")
@SecurityRequirement(name = "Bearer Authentication")
@Tag(name = "Admin Predictions", description = "Administrative endpoints for system-wide prediction history")
public class AdminPredictionController {

    private final PredictionHistoryService predictionHistoryService;

    public AdminPredictionController(PredictionHistoryService predictionHistoryService) {
        this.predictionHistoryService = predictionHistoryService;
    }

    @GetMapping
    @Operation(summary = "Get system-wide prediction history (Admin only)",
            description = "Returns paginated prediction history across all users. Requires ROLE_ADMIN.")
    public ResponseEntity<PageResponse<PredictionHistoryResponse>> getAllPredictions(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        PageResponse<PredictionHistoryResponse> response = predictionHistoryService.getAllPredictionsForAdmin(page, size);
        return ResponseEntity.ok(response);
    }
}

package com.propvalueai.backend.controller;

import com.propvalueai.backend.dto.common.PageResponse;
import com.propvalueai.backend.dto.prediction.*;
import com.propvalueai.backend.security.SecurityUserPrincipal;
import com.propvalueai.backend.service.PredictionHistoryService;
import com.propvalueai.backend.service.PredictionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/predictions")
@SecurityRequirement(name = "Bearer Authentication")
@Tag(name = "Predictions", description = "Authenticated real-estate price prediction and history endpoints")
public class PredictionController {

    private final PredictionService predictionService;
    private final PredictionHistoryService predictionHistoryService;

    public PredictionController(PredictionService predictionService,
                                PredictionHistoryService predictionHistoryService) {
        this.predictionService = predictionService;
        this.predictionHistoryService = predictionHistoryService;
    }

    @PostMapping
    @Operation(summary = "Predict single property price",
            description = "Computes ML valuation via FastAPI and persists the result against the authenticated user.")
    public ResponseEntity<PredictionResponse> predict(
            @Valid @RequestBody PropertyInputRequest request,
            @AuthenticationPrincipal SecurityUserPrincipal principal) {
        PredictionResponse response = predictionService.predict(request, principal);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/batch")
    @Operation(summary = "Predict batch property prices",
            description = "Computes ML valuation for 1 to 100 properties and persists records against the authenticated user.")
    public ResponseEntity<BatchPredictionResponse> predictBatch(
            @Valid @RequestBody BatchPropertyInputRequest request,
            @AuthenticationPrincipal SecurityUserPrincipal principal) {
        BatchPredictionResponse response = predictionService.predictBatch(request, principal);
        return ResponseEntity.ok(response);
    }

    @GetMapping
    @Operation(summary = "Get user prediction history",
            description = "Returns paginated list of prediction records owned by the authenticated caller.")
    public ResponseEntity<PageResponse<PredictionHistoryResponse>> getUserHistory(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @AuthenticationPrincipal SecurityUserPrincipal principal) {
        PageResponse<PredictionHistoryResponse> response = predictionHistoryService.getUserHistory(principal, page, size);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get prediction record by ID",
            description = "Retrieves a single prediction record. Non-admin callers can only access their own records.")
    public ResponseEntity<PredictionHistoryResponse> getPredictionById(
            @PathVariable Long id,
            @AuthenticationPrincipal SecurityUserPrincipal principal) {
        PredictionHistoryResponse response = predictionHistoryService.getPredictionById(id, principal);
        return ResponseEntity.ok(response);
    }
}

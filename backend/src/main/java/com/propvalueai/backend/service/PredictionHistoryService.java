package com.propvalueai.backend.service;

import com.propvalueai.backend.dto.common.PageResponse;
import com.propvalueai.backend.dto.prediction.PredictionHistoryResponse;
import com.propvalueai.backend.entity.PredictionRecordEntity;
import com.propvalueai.backend.exception.ResourceNotFoundException;
import com.propvalueai.backend.repository.PredictionRecordRepository;
import com.propvalueai.backend.security.SecurityUserPrincipal;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class PredictionHistoryService {

    private final PredictionRecordRepository predictionRecordRepository;

    public PredictionHistoryService(PredictionRecordRepository predictionRecordRepository) {
        this.predictionRecordRepository = predictionRecordRepository;
    }

    @Transactional(readOnly = true)
    public PageResponse<PredictionHistoryResponse> getUserHistory(SecurityUserPrincipal principal, int page, int size) {
        int safePage = Math.max(page, 0);
        int safeSize = Math.clamp(size, 1, 100);

        Pageable pageable = PageRequest.of(safePage, safeSize,
                Sort.by(Sort.Order.desc("createdAt"), Sort.Order.desc("id")));
        Page<PredictionRecordEntity> entityPage = predictionRecordRepository.findByUserId(principal.getId(), pageable);

        Page<PredictionHistoryResponse> dtoPage = entityPage.map(PredictionHistoryResponse::fromEntity);
        return PageResponse.fromPage(dtoPage);
    }

    @Transactional(readOnly = true)
    public PredictionHistoryResponse getPredictionById(Long id, SecurityUserPrincipal principal) {
        PredictionRecordEntity record = predictionRecordRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Prediction record not found with id: " + id));

        // Enforce ownership: record must belong to the caller, unless caller is an admin
        boolean isAdmin = principal.getAuthorities().stream()
                .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));

        if (!isAdmin && (record.getUser() == null || !record.getUser().getId().equals(principal.getId()))) {
            throw new AccessDeniedException("Access denied: You do not own this prediction record.");
        }

        return PredictionHistoryResponse.fromEntity(record);
    }

    @Transactional(readOnly = true)
    public PageResponse<PredictionHistoryResponse> getAllPredictionsForAdmin(int page, int size) {
        int safePage = Math.max(page, 0);
        int safeSize = Math.clamp(size, 1, 100);

        Pageable pageable = PageRequest.of(safePage, safeSize,
                Sort.by(Sort.Order.desc("createdAt"), Sort.Order.desc("id")));
        Page<PredictionRecordEntity> entityPage = predictionRecordRepository.findAll(pageable);

        Page<PredictionHistoryResponse> dtoPage = entityPage.map(PredictionHistoryResponse::fromEntity);
        return PageResponse.fromPage(dtoPage);
    }
}

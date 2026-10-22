package com.propvalueai.backend.service;

import com.propvalueai.backend.dto.prediction.*;
import com.propvalueai.backend.entity.PredictionRecordEntity;
import com.propvalueai.backend.entity.UserEntity;
import com.propvalueai.backend.exception.ResourceNotFoundException;
import com.propvalueai.backend.repository.PredictionRecordRepository;
import com.propvalueai.backend.repository.UserRepository;
import com.propvalueai.backend.security.SecurityUserPrincipal;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

@Service
public class PredictionService {

    public static final String MANDATORY_DISCLAIMER =
            "PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.";

    private final FastApiClientService fastApiClientService;
    private final PredictionRecordRepository predictionRecordRepository;
    private final UserRepository userRepository;

    public PredictionService(FastApiClientService fastApiClientService,
                             PredictionRecordRepository predictionRecordRepository,
                             UserRepository userRepository) {
        this.fastApiClientService = fastApiClientService;
        this.predictionRecordRepository = predictionRecordRepository;
        this.userRepository = userRepository;
    }

    @Transactional
    public PredictionResponse predict(PropertyInputRequest request, SecurityUserPrincipal principal) {
        validatePropertyInput(request);

        UserEntity user = userRepository.findById(principal.getId())
                .orElseThrow(() -> new ResourceNotFoundException("Authenticated user record not found."));

        FastApiPredictRequest fastApiRequest = FastApiPredictRequest.fromPropertyInput(request);
        FastApiPredictResponse fastApiResponse = fastApiClientService.predict(fastApiRequest);

        PredictionRecordEntity record = new PredictionRecordEntity();
        record.setUser(user);
        record.setTotalSqftInput(request.getTotalSqftAsString());
        record.setSizeInput(request.getSizeAsString());
        record.setBathInput(request.getBath());
        record.setBalconyInput(request.getBalcony());
        record.setAreaTypeInput(request.getAreaType());
        record.setPredictedPriceLakhs(fastApiResponse.getPredictedPrice());
        record.setTargetUnit(fastApiResponse.getTargetUnit() != null ? fastApiResponse.getTargetUnit() : "Lakhs INR");
        record.setModelName(fastApiResponse.getModelName() != null ? fastApiResponse.getModelName() : "Random Forest");
        record.setModelVersion(fastApiResponse.getModelVersion() != null ? fastApiResponse.getModelVersion() : "1.0.0");
        record.setFastapiPredictionId(fastApiResponse.getPredictionId());
        record.setDisclaimer(MANDATORY_DISCLAIMER);
        record.setStatus("SUCCESS");

        PredictionRecordEntity saved = predictionRecordRepository.save(record);

        return new PredictionResponse(
                saved.getId(),
                saved.getPredictedPriceLakhs(),
                saved.getTargetUnit(),
                saved.getModelName(),
                saved.getModelVersion(),
                saved.getFastapiPredictionId(),
                saved.getDisclaimer(),
                saved.getCreatedAt()
        );
    }

    @Transactional
    public BatchPredictionResponse predictBatch(BatchPropertyInputRequest batchRequest, SecurityUserPrincipal principal) {
        if (batchRequest.getProperties() == null || batchRequest.getProperties().isEmpty()) {
            throw new IllegalArgumentException("Batch prediction request must contain at least one property input.");
        }

        UserEntity user = userRepository.findById(principal.getId())
                .orElseThrow(() -> new ResourceNotFoundException("Authenticated user record not found."));

        List<FastApiPredictRequest> fastApiRequests = new ArrayList<>();
        for (PropertyInputRequest input : batchRequest.getProperties()) {
            validatePropertyInput(input);
            fastApiRequests.add(FastApiPredictRequest.fromPropertyInput(input));
        }

        FastApiBatchPredictResponse fastApiBatchResponse = fastApiClientService.predictBatch(fastApiRequests);

        List<PredictionResponse> results = new ArrayList<>();
        for (int i = 0; i < fastApiBatchResponse.getPredictions().size(); i++) {
            FastApiPredictResponse item = fastApiBatchResponse.getPredictions().get(i);
            PropertyInputRequest originalInput = batchRequest.getProperties().get(i);

            PredictionRecordEntity record = new PredictionRecordEntity();
            record.setUser(user);
            record.setTotalSqftInput(originalInput.getTotalSqftAsString());
            record.setSizeInput(originalInput.getSizeAsString());
            record.setBathInput(originalInput.getBath());
            record.setBalconyInput(originalInput.getBalcony());
            record.setAreaTypeInput(originalInput.getAreaType());
            record.setPredictedPriceLakhs(item.getPredictedPrice());
            record.setTargetUnit(item.getTargetUnit() != null ? item.getTargetUnit() : "Lakhs INR");
            record.setModelName(item.getModelName() != null ? item.getModelName() : "Random Forest");
            record.setModelVersion(item.getModelVersion() != null ? item.getModelVersion() : "1.0.0");
            record.setFastapiPredictionId(item.getPredictionId());
            record.setDisclaimer(MANDATORY_DISCLAIMER);
            record.setStatus("SUCCESS");

            PredictionRecordEntity saved = predictionRecordRepository.save(record);

            results.add(new PredictionResponse(
                    saved.getId(),
                    saved.getPredictedPriceLakhs(),
                    saved.getTargetUnit(),
                    saved.getModelName(),
                    saved.getModelVersion(),
                    saved.getFastapiPredictionId(),
                    saved.getDisclaimer(),
                    saved.getCreatedAt()
            ));
        }

        return new BatchPredictionResponse(
                results,
                results.size(),
                fastApiBatchResponse.getModelName(),
                fastApiBatchResponse.getModelVersion(),
                MANDATORY_DISCLAIMER
        );
    }

    private void validatePropertyInput(PropertyInputRequest request) {
        if (request.getPrice() != null) {
            throw new IllegalArgumentException("Target variable 'price' is strictly forbidden in prediction requests to prevent data leakage.");
        }
        if (request.getTotalSqft() == null || request.getTotalSqftAsString().isBlank()) {
            throw new IllegalArgumentException("Field 'total_sqft' is required and must not be blank.");
        }
    }
}

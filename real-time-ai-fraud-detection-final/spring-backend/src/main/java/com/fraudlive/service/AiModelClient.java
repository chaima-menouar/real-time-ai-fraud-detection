package com.fraudlive.service;

import com.fraudlive.dto.AiPredictionResponse;
import com.fraudlive.exception.ModelUnavailableException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Component
public class AiModelClient {
    private final RestTemplate restTemplate;
    private final String predictUrl;

    public AiModelClient(RestTemplate restTemplate, @Value("${app.ai-service-url}") String baseUrl) {
        this.restTemplate = restTemplate;
        this.predictUrl = baseUrl.replaceAll("/+$", "") + "/predict";
    }

    public AiPredictionResponse predict(String content) {
        try {
            AiPredictionResponse response = restTemplate.postForObject(
                    predictUrl,
                    Map.of("text", content),
                    AiPredictionResponse.class
            );
            if (response == null
                    || response.category() == null
                    || response.category().isBlank()
                    || response.modelVersion() == null
                    || response.modelVersion().isBlank()
                    || !Double.isFinite(response.confidence())
                    || response.confidence() < 0.0
                    || response.confidence() > 1.0) {
                throw new ModelUnavailableException("AI service returned an incomplete response", null);
            }
            return response;
        } catch (ModelUnavailableException exception) {
            throw exception;
        } catch (RestClientException exception) {
            throw new ModelUnavailableException("AI model is unavailable; the comment was not classified", exception);
        }
    }
}

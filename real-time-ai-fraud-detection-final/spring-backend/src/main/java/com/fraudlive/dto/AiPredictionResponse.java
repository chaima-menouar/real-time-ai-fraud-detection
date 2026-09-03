package com.fraudlive.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record AiPredictionResponse(
        String category,
        boolean risk,
        double confidence,
        @JsonProperty("model_version") String modelVersion
) {
}

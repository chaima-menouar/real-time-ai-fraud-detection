package com.fraudlive.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CreateLiveRequest(
        @NotBlank @Size(max = 120) String title
) {
}

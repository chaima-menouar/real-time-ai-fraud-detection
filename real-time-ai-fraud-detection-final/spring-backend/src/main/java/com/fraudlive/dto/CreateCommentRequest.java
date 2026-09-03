package com.fraudlive.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CreateCommentRequest(
        @NotBlank @Size(max = 80) String author,
        @NotBlank @Size(min = 3, max = 2000) String content
) {
}

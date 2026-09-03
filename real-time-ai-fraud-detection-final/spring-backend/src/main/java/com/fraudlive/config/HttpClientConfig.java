package com.fraudlive.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

@Configuration
public class HttpClientConfig {
    @Bean
    RestTemplate restTemplate(
            RestTemplateBuilder builder,
            @Value("${app.ai-connect-timeout-ms}") long connectTimeout,
            @Value("${app.ai-read-timeout-ms}") long readTimeout
    ) {
        return builder
                .connectTimeout(Duration.ofMillis(connectTimeout))
                .readTimeout(Duration.ofMillis(readTimeout))
                .build();
    }
}

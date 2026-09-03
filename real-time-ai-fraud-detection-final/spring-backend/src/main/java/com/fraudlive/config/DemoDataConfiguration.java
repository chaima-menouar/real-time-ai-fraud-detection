package com.fraudlive.config;

import com.fraudlive.model.Live;
import com.fraudlive.model.LiveStatus;
import com.fraudlive.repository.LiveRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DemoDataConfiguration {
    @Bean
    @ConditionalOnProperty(name = "app.demo-data-enabled", havingValue = "true")
    CommandLineRunner seedDemoLive(LiveRepository repository) {
        return args -> {
            if (repository.count() == 0) {
                Live live = new Live("Responsible AI & Online Safety — Demo Live");
                live.setStatus(LiveStatus.ACTIVE);
                repository.save(live);
            }
        };
    }
}

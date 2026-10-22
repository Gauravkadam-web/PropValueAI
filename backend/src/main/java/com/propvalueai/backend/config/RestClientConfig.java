package com.propvalueai.backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestClient;

import java.time.Duration;

@Configuration
public class RestClientConfig {

    private final AppProperties appProperties;

    public RestClientConfig(AppProperties appProperties) {
        this.appProperties = appProperties;
    }

    @Bean
    public RestClient fastApiRestClient() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(Duration.ofMillis(appProperties.getFastapi().getConnectTimeoutMs()));
        factory.setReadTimeout(Duration.ofMillis(appProperties.getFastapi().getReadTimeoutMs()));

        return RestClient.builder()
                .baseUrl(appProperties.getFastapi().getBaseUrl())
                .requestFactory(factory)
                .build();
    }
}

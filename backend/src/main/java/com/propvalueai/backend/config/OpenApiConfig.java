package com.propvalueai.backend.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    private static final String SECURITY_SCHEME_NAME = "Bearer Authentication";

    @Bean
    public OpenAPI propValueAiOpenApi() {
        return new OpenAPI()
                .info(new Info()
                        .title("PropValueAI Backend API")
                        .description("Core Spring Boot application API for PropValueAI Real Estate Price Prediction platform. " +
                                "Provides user authentication, prediction orchestration via ML inference, prediction history persistence, and administrative controls.")
                        .version("1.0.0")
                        .contact(new Contact().name("PropValueAI Engineering").url("https://github.com/Gauravkadam-web/PropValueAI"))
                        .license(new License().name("Educational Use").url("https://github.com/Gauravkadam-web/PropValueAI/blob/main/LICENSE")))
                .addSecurityItem(new SecurityRequirement().addList(SECURITY_SCHEME_NAME))
                .components(new Components()
                        .addSecuritySchemes(SECURITY_SCHEME_NAME,
                                new SecurityScheme()
                                        .name(SECURITY_SCHEME_NAME)
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")
                                        .description("Enter your JWT token obtained from /api/v1/auth/login to authenticate.")));
    }
}

package com.propvalueai.backend.config;

import com.propvalueai.backend.entity.Role;
import com.propvalueai.backend.entity.UserEntity;
import com.propvalueai.backend.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
public class AdminInitializer implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(AdminInitializer.class);

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AppProperties appProperties;

    public AdminInitializer(UserRepository userRepository,
                            PasswordEncoder passwordEncoder,
                            AppProperties appProperties) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.appProperties = appProperties;
    }

    @Override
    public void run(String... args) {
        String adminEmail = appProperties.getAdmin().getEmail();
        String adminPassword = appProperties.getAdmin().getPassword();

        if (!StringUtils.hasText(adminEmail) || !StringUtils.hasText(adminPassword)) {
            log.info("No administrative credentials supplied via PROPVALUEAI_ADMIN_EMAIL / PROPVALUEAI_ADMIN_PASSWORD. Skipping automatic administrator provisioning.");
            return;
        }

        String normalizedEmail = adminEmail.toLowerCase().trim();
        if (userRepository.existsByEmail(normalizedEmail)) {
            log.info("Administrator account '{}' already exists. Preserving existing record.", normalizedEmail);
            return;
        }

        String firstName = StringUtils.hasText(appProperties.getAdmin().getFirstName()) ? appProperties.getAdmin().getFirstName() : "System";
        String lastName = StringUtils.hasText(appProperties.getAdmin().getLastName()) ? appProperties.getAdmin().getLastName() : "Administrator";

        UserEntity admin = new UserEntity(
                normalizedEmail,
                passwordEncoder.encode(adminPassword),
                firstName,
                lastName,
                Role.ROLE_ADMIN
        );

        userRepository.save(admin);
        log.info("Successfully provisioned initial administrator account for '{}' via environment configuration.", normalizedEmail);
    }
}

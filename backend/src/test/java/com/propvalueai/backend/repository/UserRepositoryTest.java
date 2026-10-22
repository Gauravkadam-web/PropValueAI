package com.propvalueai.backend.repository;

import com.propvalueai.backend.entity.Role;
import com.propvalueai.backend.entity.UserEntity;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldSaveAndFindUserByEmail() {
        UserEntity user = new UserEntity(
                "gaurav@example.com",
                "$2a$12$eX4mP1eHaShVaLuE1234567890123456789012345678901234567",
                "Gaurav",
                "Kadam",
                Role.ROLE_USER
        );

        UserEntity saved = userRepository.save(user);

        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getUpdatedAt()).isNotNull();

        Optional<UserEntity> found = userRepository.findByEmail("gaurav@example.com");
        assertThat(found).isPresent();
        assertThat(found.get().getFirstName()).isEqualTo("Gaurav");
        assertThat(found.get().getRole()).isEqualTo(Role.ROLE_USER);

        assertThat(userRepository.existsByEmail("gaurav@example.com")).isTrue();
        assertThat(userRepository.existsByEmail("nonexistent@example.com")).isFalse();
    }
}

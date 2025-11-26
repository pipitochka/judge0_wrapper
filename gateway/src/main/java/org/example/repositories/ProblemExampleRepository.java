package org.example.repositories;

import org.example.domain.ProblemExample;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProblemExampleRepository extends JpaRepository<ProblemExample, Long> {
}

package org.example.repositories;

import org.example.domain.SolutionComment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface SolutionCommentRepository extends JpaRepository<SolutionComment, Long> {

    @Query("SELECT sc FROM SolutionComment sc WHERE sc.user.id = :userId AND sc.task.id = :taskId")
    Optional<SolutionComment> findByUserIdAndTaskId(@Param("userId") Long userId,
                                                    @Param("taskId") Long taskId);

}

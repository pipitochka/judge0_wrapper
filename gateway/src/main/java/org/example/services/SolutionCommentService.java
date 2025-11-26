package org.example.services;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.example.domain.SolutionComment;
import org.example.repositories.SolutionCommentRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@Transactional
@RequiredArgsConstructor
public class SolutionCommentService {

    private final SolutionCommentRepository solutionCommentRepository;

    /**
     * Добавить ответ на вопрос
     */
    public boolean addAnswer(Long userId, Long taskId, String answer) {
        try {
            // Находим комментарий по userId и taskId
            Optional<SolutionComment> commentOpt = solutionCommentRepository
                    .findByUserIdAndTaskId(userId, taskId);

            if (commentOpt.isPresent()) {
                SolutionComment comment = commentOpt.get();
                comment.setAnswer(answer);
                solutionCommentRepository.save(comment);

                log.info("Answer added for user {} task {}", userId, taskId);
                return true;
            } else {
                log.warn("No question found for user {} task {}", userId, taskId);
                return false;
            }

        } catch (Exception e) {
            log.error("Error adding answer: {}", e.getMessage());
            return false;
        }
    }


}
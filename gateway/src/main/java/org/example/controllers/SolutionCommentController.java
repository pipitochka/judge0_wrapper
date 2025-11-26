package org.example.controllers;


import lombok.RequiredArgsConstructor;
import org.example.domain.SolutionComment;
import org.example.services.SolutionCommentService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/comments")
@RequiredArgsConstructor
public class SolutionCommentController {

    private final SolutionCommentService solutionCommentService;

    /**
     * POST /api/comments/answer - Добавить ответ на вопрос
     */
    @PostMapping("/answer")
    public ResponseEntity<String> addAnswer(
            @RequestParam Long userId,
            @RequestParam Long taskId,
            @RequestParam String answer) {

        boolean success = solutionCommentService.addAnswer(userId, taskId, answer);

        if (success) {
            return ResponseEntity.ok("Answer added successfully");
        } else {
            return ResponseEntity.badRequest().body("No question found for this user and task");
        }
    }

}
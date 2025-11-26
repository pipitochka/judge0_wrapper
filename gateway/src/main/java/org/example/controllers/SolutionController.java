package org.example.controllers;

import lombok.RequiredArgsConstructor;
import org.example.dto.SolutionResult;
import org.example.services.SolutionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/solutions")
@RequiredArgsConstructor
public class SolutionController {

    private final SolutionService solutionService;

    @PostMapping("/check")
    public ResponseEntity<SolutionResult> checkSolution(
            @RequestParam Long userId,
            @RequestParam Long taskId,
            @RequestParam String code,
            @RequestParam(defaultValue = "JAVA") String language) {

        SolutionResult result = solutionService.checkSolution(userId, taskId, code, language);
        return ResponseEntity.ok(result);
    }
}

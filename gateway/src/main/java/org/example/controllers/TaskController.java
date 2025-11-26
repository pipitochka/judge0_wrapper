package org.example.controllers;

import lombok.RequiredArgsConstructor;
import org.example.domain.Task;
import org.example.services.TaskService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/tasks")
@RequiredArgsConstructor
public class TaskController {

    private final TaskService taskService;

    @GetMapping("/next/{userId}")
    public ResponseEntity<Task> getNextTask(@PathVariable Long userId) {
        return taskService.getNextTask(userId)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/current/{userId}")
    public ResponseEntity<Task> getCurrentTask(@PathVariable Long userId) {
        return taskService.getCurrentTask(userId)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}

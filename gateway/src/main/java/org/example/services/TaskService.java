package org.example.services;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.example.domain.Task;
import org.example.domain.User;
import org.example.dto.TaskResponseDto;
import org.example.repositories.TaskRepository;
import org.example.repositories.UserRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Optional;

import static org.example.dto.TaskMapper.fromDto;

@Service
@Transactional
@RequiredArgsConstructor
public class TaskService {

    private final TaskRepository taskRepository;

    private final UserRepository userRepository;

    private final RestTemplate restTemplate;

    private final String taskCheckerUrl = "http://task-checker:8000";

    public Optional<Task> getNextTask(Long userId) {
        try {
            String url = taskCheckerUrl + "/api/tasks/" + userId;

            ResponseEntity<TaskResponseDto> response = restTemplate.getForEntity(
                    url,
                    TaskResponseDto.class
            );

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                TaskResponseDto externalTask = response.getBody();
                Task task = fromDto(externalTask);
                Task savedTask = taskRepository.save(task);

                User user = userRepository.findById(userId)
                        .orElseThrow(() -> new RuntimeException("User not found"));
                user.setCurrentTask(savedTask);
                userRepository.save(user);

                return Optional.of(savedTask);
            }

            return Optional.empty();

        } catch (Exception e) {
            System.err.println("Failed to get task from task-checker: " + e.getMessage());
            return Optional.empty();
        }
    }

    public Optional<Task> getCurrentTask(Long userId){
        try {
            return userRepository.findById(userId)
                    .map(User::getCurrentTask);
        } catch (Exception e) {
            return Optional.empty();
        }
    }
}

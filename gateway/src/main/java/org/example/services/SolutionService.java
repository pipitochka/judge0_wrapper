package org.example.services;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.example.domain.Solution;
import org.example.domain.SolutionComment;
import org.example.domain.Task;
import org.example.domain.User;
import org.example.dto.Judge0SubmissionRequestDto;
import org.example.dto.Judge0SubmissionResponseDto;
import org.example.dto.SolutionResult;
import org.example.repositories.SolutionCommentRepository;
import org.example.repositories.SolutionRepository;
import org.example.repositories.TaskRepository;
import org.example.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;


@Slf4j
@Service
@Transactional
@RequiredArgsConstructor
public class SolutionService {

    private final SolutionRepository solutionRepository;
    private final UserRepository userRepository;
    private final TaskRepository taskRepository;
    private final SolutionCommentRepository solutionCommentRepository;
    private final RestTemplate restTemplate;

    @Value("${app.judge0.url:http://judge0-server:2358}")
    private String judge0Url;

    @Value("${app.scibox.url:https://llm.t1v.scibox.tech/v1}")
    private String sciBoxUrl;

    @Value("${app.scibox.api-key}")
    private String sciBoxApiKey;

    @Transactional
    public SolutionResult checkSolution(Long userId, Long taskId, String code, String language) {
        try {
            // 1. Находим пользователя и задачу
            User user = userRepository.findById(userId)
                    .orElseThrow(() -> new RuntimeException("User not found"));
            Task task = taskRepository.findById(taskId)
                    .orElseThrow(() -> new RuntimeException("Task not found"));

            Solution solution = new Solution();
            solution.setUser(user);
            solution.setTask(task);
            solution.setText(code);
            solution.setLanguage(language);

            Solution savedSolution = solutionRepository.save(solution);

            // 2. Отправляем в Judge0
            Judge0SubmissionRequestDto judge0Request = new Judge0SubmissionRequestDto();
            judge0Request.setTask_id(taskId);
            judge0Request.setAnswer(code);
            judge0Request.setLanguage_id(mapLanguageToId(language));

            String judge0Url = this.judge0Url + "/api/submissions/";
            Map<String, Object> response = restTemplate.postForObject(judge0Url, judge0Request, Map.class);

            Long submissionId;
            if (response != null && response.containsKey("id")) {
                submissionId = Long.valueOf(response.get("id").toString());
            } else {
                throw new RuntimeException("Error solution check");
            }

            // 3. Получаем результат от Judge0
            Judge0SubmissionResponseDto finalResult = pollSubmissionResult(submissionId);

            // 4. Анализируем результат и обращаемся к AI
            String aiResponse = analyzeWithAI(finalResult, code, task);

            SolutionResult solutionResult = new SolutionResult();
            solutionResult.setComment(aiResponse);
            solutionResult.setCompleted(Objects.equals(finalResult.getStatus(), "Failed") ? false : true);
            if (solutionResult.isCompleted()){
                SolutionComment comment = new SolutionComment();
                comment.setUser(user);
                comment.setTask(task);
                comment.setQuestion(aiResponse);
                comment.setAnswer("");
                solutionCommentRepository.save(comment);

            }
            savedSolution.setAiComment(aiResponse);
            savedSolution.setCompleted(solutionResult.isCompleted());
            solutionRepository.save(savedSolution);

            return solutionResult;

        } catch (Exception e) {
            log.error("Error checking solution: {}", e.getMessage());
            return new SolutionResult(false, "Error: " + e.getMessage())  ;
        }
    }

    private Judge0SubmissionResponseDto pollSubmissionResult(Long submissionId) {
        int maxAttempts = 30;
        int delayMs = 1000;

        for (int attempt = 0; attempt < maxAttempts; attempt++) {
            try {
                if (attempt > 0) {
                    Thread.sleep(delayMs);
                }

                String url = judge0Url + "/api/submissions/" + submissionId;
                Judge0SubmissionResponseDto result = restTemplate.getForObject(url, Judge0SubmissionResponseDto.class);

                if (result != null) {
                    String status = result.getStatus();
                    log.debug("Polling attempt {}: Status = {}", attempt + 1, status);

                    if (status != null && !"pending".equalsIgnoreCase(status) &&
                            !"in progress".equalsIgnoreCase(status) &&
                            !"processing".equalsIgnoreCase(status)) {
                        log.info("Submission {} completed with status: {}", submissionId, status);
                        return result;
                    }
                }

            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Polling interrupted");
            } catch (Exception e) {
                log.warn("Error during polling attempt {}: {}", attempt + 1, e.getMessage());
            }
        }

        throw new RuntimeException("Timeout waiting for submission result after " + maxAttempts + " attempts");
    }

    /**
     * Анализ решения с помощью AI
     */
    private String analyzeWithAI(Judge0SubmissionResponseDto judgeResult, String code, Task task) {
        try {
            String status = judgeResult.getStatus();
            String prompt;

            if ("Accepted".equalsIgnoreCase(status) || "Success".equalsIgnoreCase(status)) {
                // Решение прошло - генерируем вопросы
                prompt = String.format(
                        "Сгенерируй 3 технических вопроса по этому решению задачи. " +
                                "Задача: %s\n\nРешение:\n%s\n\n" +
                                "Вопросы должны проверять понимание алгоритма, сложности и возможных улучшений.",
                        task.getText(), code
                );
            } else {
                // Решение не прошло - просим помочь
                prompt = String.format(
                        "Проанализируй это решение задачи и подскажи, что не так. " +
                                "Задача: %s\n\nРешение:\n%s\n\n" +
                                "Статус от тестирующей системы: %s\n" +
                                "Дай конкретные рекомендации по исправлению.",
                        task.getText(), code, status
                );
            }

            // Отправляем запрос в SciBox
            return callSciBoxAPI(prompt);

        } catch (Exception e) {
            log.error("Error analyzing with AI: {}", e.getMessage());
            return "AI analysis failed: " + e.getMessage();
        }
    }

    /**
     * Прямой запрос к SciBox API
     */
    private String callSciBoxAPI(String userMessage) {
         {
            // Формируем запрос
            Map<String, Object> request = new HashMap<>();
            request.put("model", "qwen3-32b-awq");
            request.put("temperature", 0.7);
            request.put("max_tokens", 500);
            request.put("stream", false);

            // Формируем messages
            List<Map<String, String>> messages = new ArrayList<>();

            Map<String, String> systemMessage = new HashMap<>();
            systemMessage.put("role", "system");
            systemMessage.put("content", "Ты опытный технический интервьюер и ментор по программированию.");

            Map<String, String> userMessageMap = new HashMap<>();
            userMessageMap.put("role", "user");
            userMessageMap.put("content", userMessage);

            messages.add(systemMessage);
            messages.add(userMessageMap);
            request.put("messages", messages);

            // Настраиваем заголовки
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", "Bearer " + sciBoxApiKey);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);

            // Отправляем запрос
            String url = sciBoxUrl + "/chat/completions";
            Map<String, Object> response = restTemplate.postForObject(url, entity, Map.class);

            // Извлекаем ответ
            if (response != null && response.containsKey("choices")) {
                List<Map<String, Object>> choices = (List<Map<String, Object>>) response.get("choices");
                if (!choices.isEmpty()) {
                    Map<String, Object> firstChoice = choices.get(0);
                    Map<String, Object> message = (Map<String, Object>) firstChoice.get("message");
                    return (String) message.get("content");
                }
            }

            return "No response from AI";

        }
    }

    private String mapLanguageToId(String language) {
        return switch (language.toUpperCase()) {
            case "JAVA" -> "62";
            case "PYTHON" -> "71";
            case "JAVASCRIPT" -> "63";
            case "CPP" -> "54";
            case "C" -> "50";
            case "GO" -> "60";
            case "RUST" -> "73";
            default -> "62";
        };
    }
}

package org.example.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Judge0SubmissionRequestDto {
    private Long task_id;
    private String answer;
    private String language_id;
}
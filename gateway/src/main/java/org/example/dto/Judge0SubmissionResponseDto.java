package org.example.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Judge0SubmissionResponseDto {
    private Long id;
    private Long task_id;
    private String status;
    private String answer;
    private List<TestCaseResultDto> testcase_results;
}

@Data
@NoArgsConstructor
@AllArgsConstructor
class TestCaseResultDto {
    private String stdin;
    private String stdout;
    private String stderr;
    private String expected_answer;
    private String message;
    private String compile_output;
    private String status;
    private Integer used_memory;
    private String used_time;
}
package org.example.dto;

import org.example.domain.ProblemExample;
import org.example.domain.Task;

import java.util.List;
import java.util.stream.Collectors;

public class TaskMapper {

    public static Task fromDto(TaskResponseDto taskResponseDto) {
        Task task = new Task();
        task.setId(taskResponseDto.getId());
        task.setText(taskResponseDto.getContent());

        if (taskResponseDto.getTests() != null) {
            List<ProblemExample> examples = taskResponseDto.getTests().stream()
                    .map(test -> {
                        ProblemExample example = new ProblemExample();
                        example.setInput(test.getStdin());
                        example.setOutput(test.getExpected());
                        example.setTask(task); // устанавливаем связь
                        return example;
                    })
                    .collect(Collectors.toList());
            task.setExamples(examples);
        }

        return task;
    }

    public static TaskResponseDto toDto(Task task) {
        List<TestCaseDto> tests = task.getExamples().stream()
                .map(example -> new TestCaseDto(example.getInput(), example.getOutput()))
                .collect(Collectors.toList());

        return new TaskResponseDto(task.getId(), task.getText(), tests);
    }
}

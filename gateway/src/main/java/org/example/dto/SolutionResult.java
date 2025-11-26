package org.example.dto;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Setter
@Getter
public class SolutionResult {
    boolean isCompleted;

    String comment;
}

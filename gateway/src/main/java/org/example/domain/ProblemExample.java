package org.example.domain;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "problem_examples")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ProblemExample {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "problem_id")
    private Task task;

    @Column(name = "input_example")
    private String input;

    @Column(name = "output_example")
    private String output;
}

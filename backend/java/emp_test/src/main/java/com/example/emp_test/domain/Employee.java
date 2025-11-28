package com.example.emp_test.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "employees")
@Getter
@Setter
@NoArgsConstructor
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "age", nullable = false)
    private Integer age;

    @Column(name = "job", nullable = false)
    private String job;

    @Column(name = "language", nullable = false)
    private String language;

    @Column(name = "pay", nullable = false)
    private Integer pay;

    public Employee(String name, int age, String job, String language, int pay) {
        this.name = name;
        this.age = age;
        this. job = job;
        this.language = language;
        this.pay = pay;
    }

}

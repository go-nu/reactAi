package com.example.emp_test.graphql;

public record EmployeeInput(
    String name,
    int age,
    String job,
    String language,
    int pay
) {}

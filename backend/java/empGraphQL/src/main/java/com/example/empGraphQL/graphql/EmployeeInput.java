package com.example.empGraphQL.graphql;

public record EmployeeInput (
    String name,
    int age,
    String job,
    String language,
    int pay
){}
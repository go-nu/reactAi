package com.example.empGraphQL.domain;

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

    private String name;
    private int age;
    private String job;
    private String language;
    private int pay;

    public Employee(String name, int age, String job, String language, int pay){
        this.name = name;
        this.age = age;
        this.job = job;
        this.language = language;
        this.pay = pay;
    }



}

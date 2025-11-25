package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity // 1. 이 클래스는 DB 테이블과 매핑된다는 뜻 (JPA 핵심)
@Table(name = "employees")
@Getter @Setter
@NoArgsConstructor // 기본 생성자 (JPA 필수)
public class Employee {

    @Id // Primary Key
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Auto Increment
    private Long id;

    @Column(length = 100, nullable = false) // String(100), nullable=False
    private String name;

    @Column(nullable = false)
    private Integer age;

    @Column(length = 100, nullable = false)
    private String job;

    @Column(length = 100) // nullable=True (기본값)
    private String language;

    @Column(length = 100, nullable = false)
    private String pay;

    public Employee(String name, Integer age, String job, String language, String pay) {
        this.name = name;
        this.age = age;
        this.job = job;
        this.language = language;
        this.pay = pay;
    }
}
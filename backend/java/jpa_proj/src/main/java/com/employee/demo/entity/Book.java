package com.employee.demo.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "books")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @OneToMany(fetch = FetchType.LAZY, mappedBy = "bId")
    private long id;

    @Column(nullable = false, length = 50)
    private String bookName;

    @Column(nullable = false)
    private Integer price;

    @Column(nullable = false, length = 50)
    private String author;

    @Column(nullable = false, length = 50)
    private String publisher;

}

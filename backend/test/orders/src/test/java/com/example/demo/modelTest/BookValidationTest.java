package com.example.demo.modelTest;

import com.example.demo.model.Book;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.validation.BeanPropertyBindingResult;
import org.springframework.validation.Validator;

import java.math.BigDecimal;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.equalTo;

@SpringBootTest
public class BookValidationTest {

    @Autowired
    private Validator validator;

    @Test
    public void testBookValidation(){
        Book book = Book.builder()
                .title("")
                .author("")
                .price(BigDecimal.valueOf(0)) // BigDecimal 사용법 수정
                .stockQuantity(-5)
                .build();

        var errors = new BeanPropertyBindingResult(book, "book");
        validator.validate(book, errors);

        assertThat(errors.getErrorCount(), equalTo(4)); // assertThat 사용법 수정
        errors.getAllErrors().forEach(error -> {
            System.out.println(error.getDefaultMessage());
        });
    }
}

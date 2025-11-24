package com.example.demo.service;

import com.example.demo.model.Book;
import com.example.demo.repository.BookRepository;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class BookServiceTest {

    @Mock
    private BookRepository bookRepository;

    @InjectMocks
    private BookService bookService;

    @Test
    public void testGetAllBooks() {
        Book book = new Book(1L, "Java Programming", "John Doe", BigDecimal.valueOf(100.0), 10, null);
        when(bookRepository.findAll()).thenReturn(List.of(book));

        List<Book> books = bookService.getAllBooks();

        assertThat(books).hasSize(1);
        assertThat(books.get(0).getTitle()).isEqualTo("Java Programming");
    }

    @Test
    public void testCreateBook() {
        Book book = new Book(1L, "Java Programming", "John Doe", BigDecimal.valueOf(100.0), 10, null);
        when(bookRepository.save(any(Book.class))).thenReturn(book);

        Book createdBook = bookService.createBook(book);

        assertThat(createdBook.getTitle()).isEqualTo("Java Programming");
    }
}

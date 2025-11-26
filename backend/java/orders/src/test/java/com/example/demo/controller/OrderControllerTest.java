package com.example.demo.controller;

import com.example.demo.model.Book;
import com.example.demo.model.Customer;
import com.example.demo.model.Order;
import com.example.demo.model.OrderStatus;
import com.example.demo.service.OrderService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
public class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private OrderService orderService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    public void testGetAllOrders() throws Exception {
        Order order = createMockOrder();
        when(orderService.getAllOrders()).thenReturn(List.of(order));

        mockMvc.perform(get("/api/orders"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].quantity").value(2));
    }

    @Test
    public void testCreateOrder() throws Exception {
        Order order = createMockOrder();

        when(orderService.createOrder(
                anyLong(),
                anyLong(),
                anyInt(),
                any(LocalDateTime.class),
                any(OrderStatus.class)
        )).thenReturn(order);

        mockMvc.perform(post("/api/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(order)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.quantity").value(2));
    }

    @Test
    public void testGetOrderById() throws Exception {
        Order order = createMockOrder();
        when(orderService.getOrderById(1L)).thenReturn(Optional.of(order));

        mockMvc.perform(get("/api/orders/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.quantity").value(2));
    }

    @Test
    public void testChangeOrderStatus() throws Exception {
        Order order = createMockOrder();
        order.setStatus(OrderStatus.COMPLETED);
        when(orderService.changeOrderStatus(1L, OrderStatus.COMPLETED)).thenReturn(order);

        mockMvc.perform(patch("/api/orders/1/status?status=COMPLETED"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("COMPLETED"));
    }

    private Order createMockOrder() {
        Customer customer = new Customer(1L, "John Doe", "john@example.com", "010-1234-5678", null);
        Book book = new Book(1L, "Java Programming", "John Doe", BigDecimal.valueOf(100.0), 10, null);
        return new Order(1L, customer, book, 2, LocalDateTime.now(), OrderStatus.PENDING);
    }
}

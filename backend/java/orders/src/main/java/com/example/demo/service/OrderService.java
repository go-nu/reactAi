package com.example.demo.service;

import com.example.demo.model.*;
import com.example.demo.repository.BookRepository;
import com.example.demo.repository.CustomerRepository;
import com.example.demo.repository.OrderCustomerViewRepository;
import com.example.demo.repository.OrderRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final BookRepository bookRepository;
    private final CustomerRepository customerRepository;
    private final OrderCustomerViewRepository orderCustomerViewRepository;

    // 모든 주문 목록 조회
    public List<Order> getAllOrders() {
        return orderRepository.findAll();
    }
    public List<OrderCustomerView> getAllOrdersView() {
        return orderCustomerViewRepository.findAll();
    }

    // 주문 ID로 주문 조회
    public Optional<Order> getOrderById(Long id) {
        return orderRepository.findById(id);
    }

    // 새 주문 생성
    public Order createOrder(Long customerId, Long bookId, int quantity, LocalDateTime orderDate, OrderStatus status) {
        if (quantity < 1) {
            throw new IllegalArgumentException("Quantity must be at least 1.");
        }

        Customer customer = customerRepository.findById(customerId)
                .orElseThrow(() -> new IllegalArgumentException("Customer not found with id: " + customerId));

        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new IllegalArgumentException("Book not found with id: " + bookId));

        Order order = new Order();
        order.setCustomer(customer);
        order.setBook(book);
        order.setQuantity(quantity);
        order.setOrderDate(orderDate != null ? orderDate : LocalDateTime.now());
        order.setStatus(status != null ? status : OrderStatus.PENDING);

        return orderRepository.save(order);
    }

    // 기존 주문 업데이트
    public Order updateOrder(Long id, Long customerId, Long bookId, int quantity, LocalDateTime orderDate, OrderStatus status) {
        return orderRepository.findById(id).map(order -> {
            if (customerId != null) {
                Customer customer = customerRepository.findById(customerId)
                        .orElseThrow(() -> new IllegalArgumentException("Customer not found with id: " + customerId));
                order.setCustomer(customer);
            }

            if (bookId != null) {
                Book book = bookRepository.findById(bookId)
                        .orElseThrow(() -> new IllegalArgumentException("Book not found with id: " + bookId));
                order.setBook(book);
            }

            if (quantity > 0) {
                order.setQuantity(quantity);
            }

            if (orderDate != null) {
                order.setOrderDate(orderDate);
            }

            if (status != null) {
                order.setStatus(status);
            }

            return orderRepository.save(order);
        }).orElseThrow(() -> new RuntimeException("Order not found with id: " + id));
    }

    // 주문 삭제
    public void deleteOrder(Long id) {
        if (!orderRepository.existsById(id)) {
            throw new RuntimeException("Order not found with id: " + id);
        }
        orderRepository.deleteById(id);
    }

    // 주문 상태 변경
    public Order changeOrderStatus(Long id, OrderStatus status) {
        return orderRepository.findById(id).map(order -> {
            order.setStatus(status);
            return orderRepository.save(order);
        }).orElseThrow(() -> new RuntimeException("Order not found with id: " + id));
    }
}

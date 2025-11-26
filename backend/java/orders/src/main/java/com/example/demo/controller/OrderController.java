package com.example.demo.controller;

import com.example.demo.model.Order;
import com.example.demo.model.OrderCustomerView;
import com.example.demo.model.OrderStatus;
import com.example.demo.service.OrderService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.Optional;


@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    // 모든 주문 조회
    @GetMapping
    public ResponseEntity<List<Order>> getAllOrders() {
        return ResponseEntity.ok(orderService.getAllOrders());
    }

    @GetMapping("/view")
    public ResponseEntity<List<OrderCustomerView>> getAllOrdersView() {
        return ResponseEntity.ok(orderService.getAllOrdersView());
    }

    // 주문 ID로 조회
    @GetMapping("/{id}")
    public ResponseEntity<Order> getOrderById(@PathVariable Long id) {
        Optional<Order> order = orderService.getOrderById(id);
        return order.map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    //새 주문 생성
    @PostMapping
    public ResponseEntity<Order> createOrder(@RequestBody Map<String, Object> orderRequest) {
        try {
            Long customerId = Long.valueOf(orderRequest.get("customer_id").toString());
            Long bookId = Long.valueOf(orderRequest.get("book_id").toString());
            int quantity = Integer.parseInt(orderRequest.get("quantity").toString());

            LocalDateTime orderDate = orderRequest.containsKey("orderDate") ?
                    LocalDateTime.parse(orderRequest.get("orderDate").toString()) :
                    LocalDateTime.now();

            OrderStatus status = orderRequest.containsKey("status") ?
                    OrderStatus.valueOf(orderRequest.get("status").toString().toUpperCase()) :
                    OrderStatus.PENDING;

            Order order = orderService.createOrder(customerId, bookId, quantity, orderDate, status);
            return new ResponseEntity<>(order, HttpStatus.CREATED);

        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    //주문 업데이트
    @PutMapping("/{id}")
    public ResponseEntity<Order> updateOrder(
            @PathVariable Long id,
            @RequestBody Map<String, Object> orderRequest) {
        try {
            Long customerId = orderRequest.containsKey("customer_id") ?
                    Long.valueOf(orderRequest.get("customer_id").toString()) : null;

            Long bookId = orderRequest.containsKey("book_id") ?
                    Long.valueOf(orderRequest.get("book_id").toString()) : null;

            int quantity = orderRequest.containsKey("quantity") ?
                    Integer.parseInt(orderRequest.get("quantity").toString()) : 0;

            LocalDateTime orderDate = orderRequest.containsKey("orderDate") ?
                    LocalDateTime.parse(orderRequest.get("orderDate").toString()) : null;

            OrderStatus status = orderRequest.containsKey("status") ?
                    OrderStatus.valueOf(orderRequest.get("status").toString().toUpperCase()) : null;

            Order updatedOrder = orderService.updateOrder(id, customerId, bookId, quantity, orderDate, status);
            return ResponseEntity.ok(updatedOrder);

        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    //주문 삭제
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteOrder(@PathVariable Long id) {
        orderService.deleteOrder(id);
        return ResponseEntity.noContent().build();
    }

    //주문 상태 변경
    @PatchMapping("/{id}/status")
    public ResponseEntity<Order> changeOrderStatus(@PathVariable Long id, @RequestParam OrderStatus status) {
        return ResponseEntity.ok(orderService.changeOrderStatus(id, status));
    }
}

package com.example.demo.service;

import com.example.demo.model.Customer;
import com.example.demo.repository.CustomerRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CustomerServiceTest {

    @Mock
    private CustomerRepository customerRepository;

    @InjectMocks
    private CustomerService customerService;

    private Customer sampleCustomer;

    @BeforeEach
    void setUp() {
        sampleCustomer = new Customer();
        sampleCustomer.setId(1L);
        sampleCustomer.setName("John Doe");
        sampleCustomer.setEmail("john.doe@example.com");
    }

    @Test
    void deleteCustomer_Success() {
        when(customerRepository.findById(1L)).thenReturn(Optional.of(sampleCustomer));

        customerService.deleteCustomer(1L);

        verify(customerRepository, times(1)).findById(1L);
        verify(customerRepository, times(1)).delete(sampleCustomer);
        verifyNoMoreInteractions(customerRepository);
    }

    @Test
    void deleteCustomer_NotFound() {
        when(customerRepository.findById(2L)).thenReturn(Optional.empty());

        assertThrows(RuntimeException.class, () -> customerService.deleteCustomer(2L));

        verify(customerRepository, times(1)).findById(2L);
        verifyNoMoreInteractions(customerRepository);
    }

    @Test
    void createCustomer_NullInput() {
        assertThrows(IllegalArgumentException.class, () -> customerService.createCustomer(null));

        verifyNoInteractions(customerRepository);
    }
}

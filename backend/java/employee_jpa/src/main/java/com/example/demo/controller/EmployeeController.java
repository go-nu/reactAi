package com.example.demo.controller;

import com.example.demo.dto.EmployeeInput;
import com.example.demo.entity.Employee;
import com.example.demo.repository.EmployeeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class EmployeeController {

    private final EmployeeRepository employeeRepository;

    // ===========================
    // 1) employees (전체 조회)
    // ===========================
    @QueryMapping(name = "employees")
    public List<Employee> employees() {
        return employeeRepository.findAll();
    }

    // ===========================
    // 2) createEmployee
    // ===========================
    @MutationMapping(name = "createEmployee")
    public Employee createEmployee(@Argument EmployeeInput input) {
        Employee employee = new Employee(
            input.getName(),
            input.getAge(),
            input.getJob(),
            input.getLanguage(),
            input.getPay()
        );
        return employeeRepository.save(employee);
    }

    // ===========================
    // 3) updateEmployee
    // ===========================
    @MutationMapping(name = "updateEmployee")
    public Employee updateEmployee(
            @Argument Long id,
            @Argument EmployeeInput input
    ) {
        Employee emp = employeeRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Not found"));

        emp.setName(input.getName());
        emp.setAge(input.getAge());
        emp.setJob(input.getJob());
        emp.setLanguage(input.getLanguage());
        emp.setPay(input.getPay());

        return employeeRepository.save(emp);
    }

    // ===========================
    // 4) deleteEmployee
    // ===========================
    @MutationMapping(name = "deleteEmployee")
    public String deleteEmployee(@Argument Long id) {
        employeeRepository.deleteById(id);
        return String.valueOf(id);
    }
}

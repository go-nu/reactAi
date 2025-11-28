package com.example.emp_test.graphql;

import com.example.emp_test.domain.Employee;
import com.example.emp_test.repository.EmployeeRepository;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

@Controller
public class EmployeeGraphQLController {

    private final EmployeeRepository employeeRepository;

    public EmployeeGraphQLController(EmployeeRepository employeeRepository) {
        this.employeeRepository = employeeRepository;
    }

    @QueryMapping
    public Employee employee(@Argument Long id) {
        return employeeRepository.findById(id).orElse(null);
    }

    @MutationMapping
    public Employee createEmployee(@Argument EmployeeInput input) {
        Employee emp = new Employee(
                input.name(),
                input.age(),
                input.job(),
                input.language(),
                input.pay()
        );
        return employeeRepository.save(emp);
    }

    @MutationMapping
    public Employee udateEmployee(@Argument Long id, @Argument EmployeeInput input) {
        Employee uEmp = employeeRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("employee not exist"));
        uEmp.setName(input.name());
        uEmp.setAge(input.age());
        uEmp.setJob(input.job());
        uEmp.setLanguage(input.language());
        uEmp.setPay(input.pay());

        return employeeRepository.save(uEmp);
    }

    @MutationMapping
    public Boolean deleteEmployee(@Argument Long id) {
        if (!employeeRepository.existsById(id)) return false;
        employeeRepository.deleteById(id);
        return true;
    }
}

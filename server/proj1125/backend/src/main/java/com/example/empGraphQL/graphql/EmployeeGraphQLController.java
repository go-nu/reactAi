package com.example.empGraphQL.graphql;

import com.example.empGraphQL.domain.Employee;
import com.example.empGraphQL.repository.EmployeeRepository;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;

@Controller
public class EmployeeGraphQLController {

    private final EmployeeRepository employeeRepository;

    public EmployeeGraphQLController(EmployeeRepository employeeRepository){
        this.employeeRepository = employeeRepository;
    }

    @QueryMapping
    public List<Employee> getEmployees(){
        return employeeRepository.findAll();
    }

    @QueryMapping
    public  Employee getEmployee(@PathVariable Long id){
        return employeeRepository.findById(id).orElse(null);
    }

    @MutationMapping
    public Employee createEmployee(@Argument EmployeeInput input){
        Employee emp = new Employee(
                input.name(),
                input.age(),
                input.job(),
                input.language(),
                input.pay()
        );
        return employeeRepository.save(emp);
    };

    @MutationMapping
    public Employee updateEmployee(@Argument Long id, @Argument EmployeeInput input){
        Employee emp = employeeRepository.findById(id)
                .orElseThrow(()-> new IllegalArgumentException("Employee not found"));
        emp.setName(input.name());
        emp.setAge(input.age());
        emp.setJob(input.job());
        emp.setLanguage(input.language());
        emp.setPay(input.pay());
        return employeeRepository.save(emp);
    }

    @MutationMapping
    public Boolean deleteEmployee(@Argument Long id){
        if(!employeeRepository.existsById(id)){
            throw new IllegalStateException("Employee not found");
        }
        employeeRepository.deleteById(id);
        return true;
    }











}

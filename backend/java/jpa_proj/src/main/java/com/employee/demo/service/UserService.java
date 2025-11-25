package com.employee.demo.service;

import com.employee.demo.entity.User;
import com.employee.demo.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> findAll() {
        return userRepository.findAll();
    }

    public User createUser(User user) {
        return userRepository.save(user);
    }

    public User getUserByName(String userName) {
        return userRepository.findByUserName(userName);
    }

    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
}

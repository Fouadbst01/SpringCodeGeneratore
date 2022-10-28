package com.exemple.MyProject.repositories;


import com.exemple.MyProject.entities.Empoyee;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EmpoyeeRepository extends JpaRepository<Empoyee,String> {
}

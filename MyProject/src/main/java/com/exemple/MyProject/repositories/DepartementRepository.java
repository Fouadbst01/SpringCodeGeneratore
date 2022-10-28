package com.exemple.MyProject.repositories;

import com.exemple.MyProject.entities.Departement;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DepartementRepository extends JpaRepository<Departement,String> {
}

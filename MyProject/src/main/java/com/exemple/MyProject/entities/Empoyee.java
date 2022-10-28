package com.exemple.MyProject.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import java.util.Date;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.*;
 import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Entity
public class Empoyee{
	@Id
	private String id;
	private String name;
	private int age;
	@ManyToOne
	Departement departement;
}

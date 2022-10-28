package com.exemple.MyProject.dtos;


import java.util.List;

import com.exemple.MyProject.dtos.DepartementDTO;
import lombok.Data;
import java.util.Date;


@Data
public class EmpoyeeDTO {
	private String id;
	private String name;
	private int age;
	DepartementDTO departementDTO;
}

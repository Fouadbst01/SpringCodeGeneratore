package com.exemple.MyProject.dtos;


import java.util.List;
import lombok.Data;
import java.util.Date;


@Data
public class DepartementDTO {
	private String id;
	private String name;
	List<EmpoyeeDTO> listEmpoyeeDTO;
}

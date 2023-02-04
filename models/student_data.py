from pydantic import BaseModel
from typing import List, Union


class Asignatura(BaseModel):
    materia: str
    calificacion: str
    periodo: str
    no_periodo: int


class Alumno(BaseModel):
    registro: str
    nombre_completo: str
    curp: str
    nombre_programa: str
    asignaturas: List[Asignatura]


class StudentDataResponse(BaseModel):
    alumno: Union[Alumno, None]
    boletas_errores: List[str]


# Conacyt
class AlumnoConacyt(BaseModel):
    registro: str
    nombre_completo: str
    curp: str
    nombre_programa: str
    pronombre: str
    pronombre_mayus: str
    letra_sexo: str
    proposicion: str
    asignaturas_semestre: List[Asignatura]
    no_asignaturas: int
    promedio_semestre: float
    semestre_actual_numero: str


class StudentConacytDataResponse(BaseModel):
    alumno: Union[AlumnoConacyt, None]
    boletas_errores: List[str]
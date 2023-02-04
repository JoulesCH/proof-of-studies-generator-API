from pydantic import BaseModel
from typing import List


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
    alumno: Alumno
    boletas_errores: list
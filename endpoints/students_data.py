from fastapi import APIRouter, Path
from pydantic import BaseModel
from typing import List

import os

from utils.students_data import get_students_data
from utils.students_data.login import login

router = APIRouter()


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

@router.get(
    path="/{student_boleta}",
    summary="Get raw data of a student",
    description="Obtiene los datos **sin limpiar** de un solo estudiante",
    response_model=StudentDataResponse,
)
async def get_student_by_boleta(student_boleta: str = Path(title="La boleta del estudiante a consultar")):
    alumno, errores = get_students_data(
        [student_boleta], 
        login(os.environ["USER"], os.environ["PASSWORD"]),
    )

    return {"alumno": alumno[0], "boletas_errores": errores}
from fastapi import APIRouter, Path

import os

from utils.students_data import get_students_data
from utils.students_data.clean_data import clean
from models.student_data import (
    StudentDataResponse, 
    StudentConacytDataResponse
)

router = APIRouter()


@router.get(
    path="/{student_boleta}",
    summary="Get raw data of a student",
    description="Obtiene los datos **sin limpiar** de un solo estudiante",
    response_model=StudentDataResponse,
)
async def get_student_by_boleta(student_boleta: str = Path(title="La boleta del estudiante a consultar")):
    alumnos, errores = get_students_data(
        [student_boleta] 
    )
    if alumnos:
        return {"alumno": alumnos[0], "boletas_errores": errores}
    else:
        return {"alumno": None, "boletas_errores": errores}

@router.get(
    path="/conacyt/{student_boleta}",
    summary="Get the data for CONACYT letter",
    description="Obtiene los datos **sin limpiar** de un solo estudiante",
    response_model=StudentConacytDataResponse,
)
async def get_conacyt_by_boleta(student_boleta: str = Path(title="La boleta del estudiante para generar constancia CONACYT")):
    alumnos, errores = get_students_data(
        [student_boleta]
    )
    if alumnos:
        data_cleanned = clean(alumnos, "CONACYT", 5)
        return {"alumno": data_cleanned[0], "boletas_errores": errores}
    else:
        return {"alumno": None, "boletas_errores": errores}
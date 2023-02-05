from fastapi import APIRouter, Path, Query
from fastapi.responses import Response
    
from utils.students_data import get_students_data
from utils.students_data.clean_data import clean
from utils.letters import createPDF

from data import getDbData


router = APIRouter()


@router.get(
    path="/conacyt/{student_boleta}",
    response_class=Response,
    responses={
        200: {
            "description": "Constancia de estudiante",
            "content": {
                "application/pdf": {
                    "example": "application/pdf"
                }
            }
        },
    },
    summary="Get the generated pdf for CONACYT letter",
    description="Obtiene la constancia en pdf **CONACYT** de un solo estudiante",
)
async def generate_pdf(
    student_boleta: str = Path(title="La boleta del estudiante para generar constancia CONACYT"),
    fecha: str = Query(title="La fecha de la constancia", example="lunes 20 de julio del 2020"),
    periodo_actual: int = Query(title="El periodo actual", example=5),
):
    alumnos, errores = get_students_data(
        [student_boleta]
    )
    if alumnos:
        data_cleanned = clean(alumnos, "CONACYT", periodo_actual)
        data_db = getDbData() #Consulta a la DB
        bytes_pdf = createPDF(
            datos=data_cleanned[0], 
            tipo_constancia="CONACYT", 
            data_db=data_db, 
            fecha=fecha, 
            periodo_actual=data_db['periodos']['lista'][periodo_actual]
        )
        return Response(bytes_pdf, media_type="application/pdf")
    else:
        return {"alumno": None, "boletas_errores": errores}


@router.get(
    path="/beifi/{student_boleta}",
    response_class=Response,
    responses={
        200: {
            "description": "Constancia de estudiante",
            "content": {
                "application/pdf": {
                    "example": "application/pdf"
                }
            }
        },
    },
    summary="Get the generated pdf for BEIFI letter",
    description="Obtiene la constancia en pdf **BEIFI** de un solo estudiante",
)
async def generate_pdf(
    student_boleta: str = Path(title="La boleta del estudiante para generar constancia BEIFI"),
    fecha: str = Query(title="La fecha de la constancia", example="lunes 20 de julio del 2020"),
    periodo_actual: int = Query(title="El periodo actual", example=5),
):
    alumnos, errores = get_students_data(
        [student_boleta]
    )
    if alumnos:
        data_cleanned = clean(alumnos, "BEIFI", periodo_actual)
        data_db = getDbData() #Consulta a la DB
        bytes_pdf = createPDF(
            datos=data_cleanned[0], 
            tipo_constancia="BEIFI", 
            data_db=data_db, 
            fecha=fecha, 
            periodo_actual=data_db['periodos']['lista'][periodo_actual]
        )
        return Response(bytes_pdf, media_type="application/pdf")
    else:
        return {"alumno": None, "boletas_errores": errores}

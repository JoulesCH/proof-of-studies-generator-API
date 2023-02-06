from fastapi import APIRouter, Path, Query
from fastapi.responses import Response
    
from utils.students_data import get_students_data
from utils.students_data.clean_data import clean
from utils.letters import createPDF

from data import getDbData

programas_no_periodos = {
    'DOCTORADO EN ENERGÍA': 8,
    'DOCTORADO EN FÍSICA DE LOS MATERIALES': 8,
    'DOCTORADO EN CIENCIAS FISICOMATEMÁTICAS': 8,
    'MAESTRÍA EN CIENCIAS FISICOMATEMÁTICAS': 5,
}

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
        periodo_actual = data_db['periodos']['lista'][periodo_actual]
        contenido = data_db['CONACYT']['contenido']
        nombre_signatario = data_db['vars']['nombre_signatario']
        puesto_signatario = data_db['vars']['puesto_signatario']
        periodo_actual_inicio_fecha = data_db['vars']['periodo_actual_inicio_fecha']
        periodo_actual_fin_fecha = data_db['vars']['periodo_actual_fin_fecha']
        fondo = data_db['vars']['fondo']
        bytes_pdf = createPDF(
            datos=data_cleanned[0], 
            tipo_constancia="CONACYT", 
            data_db=data_db, 
            fecha=fecha, 
            periodo_actual=periodo_actual,
            no_periodos_programa = programas_no_periodos[data_cleanned[0]['nombre_programa']],
            contenido=contenido,
            nombre_signatario=nombre_signatario,
            puesto_signatario=puesto_signatario,
            periodo_actual_inicio_fecha=periodo_actual_inicio_fecha,
            periodo_actual_fin_fecha=periodo_actual_fin_fecha,
            fondo=fondo
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
        periodo_actual = data_db['periodos']['lista'][periodo_actual]
        contenido = data_db['BEIFI']['contenido']
        nombre_signatario = data_db['vars']['nombre_signatario']
        puesto_signatario = data_db['vars']['puesto_signatario']
        periodo_actual_inicio_fecha = data_db['vars']['periodo_actual_inicio_fecha']
        periodo_actual_fin_fecha = data_db['vars']['periodo_actual_fin_fecha']
        fondo = data_db['vars']['fondo']
        bytes_pdf = createPDF(
            datos=data_cleanned[0], 
            tipo_constancia="BEIFI", 
            data_db=data_db, 
            fecha=fecha, 
            periodo_actual=periodo_actual,
            no_periodos_programa = programas_no_periodos[data_cleanned[0]['nombre_programa']],
            contenido=contenido,
            nombre_signatario=nombre_signatario,
            puesto_signatario=puesto_signatario,
            periodo_actual_inicio_fecha=periodo_actual_inicio_fecha,
            periodo_actual_fin_fecha=periodo_actual_fin_fecha,
            fondo=fondo
        )
        return Response(bytes_pdf, media_type="application/pdf")
    else:
        return {"alumno": None, "boletas_errores": errores}

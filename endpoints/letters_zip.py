from fastapi import APIRouter, Path, Query
from fastapi.responses import StreamingResponse
    
from utils.students_data import get_students_data
from utils.students_data.clean_data import clean
from utils.letters import createPDF
from utils.letters.zip import zip_files

from data import getDbData

programas_no_periodos = {
    'DOCTORADO EN ENERGÍA': 8,
    'DOCTORADO EN FÍSICA DE LOS MATERIALES': 8,
    'DOCTORADO EN CIENCIAS FISICOMATEMÁTICAS': 8,
    'MAESTRÍA EN CIENCIAS FISICOMATEMÁTICAS': 5,
}

router = APIRouter()


@router.get(
    path="/conacyt",
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "Constancia de estudiante",
            "content": {
                "x-zip-compressed": {
                    "example": "x-zip-compressed"
                }
            }
        },
    },
    summary="Get the generated pdfs for CONACYT letters",
    description="Obtiene la constancia en pdf **CONACYT** de un solo estudiante",
)
async def generate_zip(
    students_boleta: list = Query(title="Las boletas de los estudiantes para generar constancia CONACYT"),
    fecha: str = Query(title="La fecha de la constancia", example="lunes 20 de julio del 2020"),
    periodo_actual: int = Query(title="El periodo actual", example=5),
):
    alumnos, errores = get_students_data(
        students_boleta
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

        bytes_pdfs = [ createPDF(
                datos=data, 
                tipo_constancia="CONACYT", 
                data_db=data_db, 
                fecha=fecha, 
                periodo_actual=periodo_actual,
                no_periodos_programa = programas_no_periodos[data['nombre_programa']],
                contenido=contenido,
                nombre_signatario=nombre_signatario,
                puesto_signatario=puesto_signatario,
                periodo_actual_inicio_fecha=periodo_actual_inicio_fecha,
                periodo_actual_fin_fecha=periodo_actual_fin_fecha,
                fondo=fondo
            ) for data in data_cleanned
        ]
        zip_file = zip_files(
            bytes_pdfs=bytes_pdfs,
            datos=data_cleanned,
            tipo_constancia="CONACYT",
            semestre_actual=periodo_actual
        )
        return StreamingResponse(
            iter([zip_file.getvalue()]), 
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment; filename=Constancias_CONACYT_{periodo_actual.replace(' ', '')}.zip"}
            )
    else:
        return {"alumno": None, "boletas_errores": errores}


@router.get(
    path="/beifi",
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "Constancia de estudiante",
            "content": {
                "x-zip-compressed": {
                    "example": "x-zip-compressed"
                }
            }
        },
    },
    summary="Get the generated pdfs for BEIFI letters",
    description="Obtiene la constancia en pdf **BEIFI** de un solo estudiante",
)
async def generate_zip(
    students_boleta: list = Query(title="Las boletas de los estudiantes para generar constancia BEIFI"),
    fecha: str = Query(title="La fecha de la constancia", example="lunes 20 de julio del 2020"),
    periodo_actual: int = Query(title="El periodo actual", example=5),
):
    alumnos, errores = get_students_data(
        students_boleta
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

        bytes_pdfs = [ createPDF(
                datos=data, 
                tipo_constancia="BEIFI", 
                data_db=data_db, 
                fecha=fecha, 
                periodo_actual=periodo_actual,
                no_periodos_programa = programas_no_periodos[data['nombre_programa']],
                contenido=contenido,
                nombre_signatario=nombre_signatario,
                puesto_signatario=puesto_signatario,
                periodo_actual_inicio_fecha=periodo_actual_inicio_fecha,
                periodo_actual_fin_fecha=periodo_actual_fin_fecha,
                fondo=fondo
            ) for data in data_cleanned
        ]
        zip_file = zip_files(
            bytes_pdfs=bytes_pdfs,
            datos=data_cleanned,
            tipo_constancia="BEIFI",
            semestre_actual=periodo_actual
        )
        return StreamingResponse(
            iter([zip_file.getvalue()]), 
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment; filename=Constancias_CONACYT_{periodo_actual.replace(' ', '')}.zip"}
            )
    else:
        return {"alumno": None, "boletas_errores": errores}
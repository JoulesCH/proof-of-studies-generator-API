from fastapi import APIRouter, Body

from data import getDbData
from models.catalogs import CatalogBase, LettersBase, Vars, constancia
from typing import List

router = APIRouter()


@router.get(
    path="/",
    summary="Get all the config data",
    description="Obtiene todos los datos de configuración almacenados en la DB",
    response_model=CatalogBase,
)
async def getConfigData():
    return getDbData()


@router.get(
    path="/letters",
    summary="Get the letters config data",
    description="Obtiene todos los datos de configuración de las constancias",
    response_model=LettersBase,
)
async def getLettersData():
    data = getDbData()
    return dict(CONACYT=data['CONACYT'], BEIFI=data['BEIFI'])


@router.get(
    path="/periods/dict",
    summary="Get dictionary of periods",
    description="Obtiene todos los periodos y su identificador en diccionario",
)
async def getDictPeriods():
    data = getDbData()['periodos']
    del data['lista']
    return data


@router.get(
    path="/periods/list",
    summary="Get list of periods",
    description="Obtiene todos los periodos ordenados en lista",
    response_model=List[str],
)
async def getListPeriods():
    return getDbData()['periodos']['lista']


@router.put(
    path="/periods",
    summary="Update list of periods",
    description="Actualizar periodos",
    response_model=dict,
)
async def updatePeriods(periodos:list=Body(...,description="Lista de periodos (ordenada)", example=["2020-1", "2020-2", "2021-1"])):
    return getDbData()['periodos']


@router.put(
    path="/vars",
    summary="Update config vars",
    description="Actualizar las variables de configuración \n - fondo \n - nombre_signatario \n - puesto_signatario \n - periodo_actual_inicio_fecha \n - periodo_actual_fin_fecha",
    response_model=Vars,
)
async def updateVars(vars:Vars=Body(..., description="JSON de las variables (ordenada)")):
    return getDbData()['vars']


@router.put(
    path="/letters/conacyt",
    summary="Update CONACYT content",
    description="Actualizar el contenido de la constancia CONACYT",
    response_model=constancia,
)
async def updateCONACYT(contenido:str=Body(..., description="String del contenido")):
    return getDbData()['CONACYT']


@router.put(
    path="/letters/beifi",
    summary="Update BEIFI content",
    description="Actualizar el contenido de la constancia BEIFI",
    response_model=constancia,
)
async def updateBEIFI(contenido:str=Body(..., description="String del contenido")):
    return getDbData()['BEIFI']
from fastapi import APIRouter

from data import getDbData
from models.catalogs import CatalogBase, LettersBase

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
    description="Obtiene todos los periodos y su identificador",
    # response_model=LettersBase,
)
async def getLettersData():
    data = getDbData()['periodos']
    del data['lista']
    return data


@router.get(
    path="/periods/list",
    summary="Get list of periods",
    description="Obtiene todos los periodos y su identificador",
    # response_model=LettersBase,
)
async def getLettersData():
    return getDbData()['periodos']['lista']
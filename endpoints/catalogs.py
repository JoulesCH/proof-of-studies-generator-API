from fastapi import APIRouter, Body, File, UploadFile
from fastapi.exceptions import HTTPException
import requests

import base64
import os

from data import getDbData
from data import update_Periods, update_Vars, update_Conacyt, update_Beifi
from models.catalogs import CatalogBase, LettersBase, Vars, constancia, BackgroundReponse
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
    path="/vars",
    summary="Get all the vars data",
    description="Obtiene las variables de configuración almacenadas en la DB",
    response_model=Vars,
)
async def getConfigData():
    return getDbData()['vars']

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
    return update_Periods(periodos)['periods']


@router.put(
    path="/vars",
    summary="Update config vars",
    description="Actualizar las variables de configuración \n - fondo \n - nombre_signatario \n - puesto_signatario \n - periodo_actual_inicio_fecha \n - periodo_actual_fin_fecha",
    response_model=Vars,
)
async def updateVars(vars:Vars=Body(..., description="JSON de las variables (ordenada)")):
    return update_Vars(vars)['vars']


@router.put(
    path="/letters/conacyt",
    summary="Update CONACYT content",
    description="Actualizar el contenido de la constancia CONACYT",
    response_model=constancia,
)
async def updateCONACYT(contenido:str=Body(..., description="String del contenido")):
    return update_Conacyt(contenido)['CONACYT']


@router.put(
    path="/letters/beifi",
    summary="Update BEIFI content",
    description="Actualizar el contenido de la constancia BEIFI",
    response_model=constancia,
)
async def updateBEIFI(contenido:str=Body(..., description="String del contenido")):
    return update_Beifi(contenido)['BEIFI']


@router.post(
    '/letters/background',
    summary="Upload letter background image",
    description="Subir imagen de fondo para las constancias",
    response_model=BackgroundReponse,
)
async def uploadBackground(background:UploadFile = File(..., description="Imagen de fondo")):
    # upload background image to imgbb
    file = background.file.read()
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": os.environ['IMGBB_KEY'],
        "image": base64.b64encode(file),
    }
    response = requests.request("POST", url, data=payload)
    if response.status_code == 200:
        background = response.json()['data']
        return {"url": background['url']}	
    raise HTTPException(status_code=500, detail="Error al subir la imagen")
from pydantic import BaseModel


class constancia(BaseModel):
    contenido: str
    datos_plantilla: dict

class Vars(BaseModel):
    puesto_signatario: str
    nombre_signatario: str
    periodo_actual_fin_fecha: str
    periodo_actual_inicio_fecha: str
    fondo: str

class CatalogBase(BaseModel):
    BEIFI: constancia
    CONACYT: constancia
    periodos: dict
    vars: Vars

class LettersBase(BaseModel):
    BEIFI: constancia
    CONACYT: constancia

class BackgroundReponse(BaseModel):
    url: str
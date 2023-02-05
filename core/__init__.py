from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

'''
⚠: With bugs
✅: Done
❌: Not done
🚧: In progress
'''

load_dotenv(
    dotenv_path=".env.local",
)
description = """
# API del **Sistema de Generador de Constancias de Posgrado**
## Datos de estudiante
- **Obtener datos crudos de un solo estudiante** ✅
- **Obtener datos limpios (preparados) para una constancia de un solo estudiante** ✅
- **Obtener datos crudos de muchos estudiantes** ❌
- **Obtener datos limpios (preparados para una constancia) de muchos estudiantes** ❌
## Generar constancias
- **Generar constancias BEIFI** ✅
- **Generar constancias CONACYT** ✅
## Catálogos
- **Obtener catálogos** 🚧
- **Modificar catálogos** ❌

"""

app = FastAPI(
    title="SGC",
    description=description,
    version="1.0.0",
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from endpoints import api_router 

app.include_router(api_router, prefix="/v1")
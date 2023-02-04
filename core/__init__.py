from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

description = """
API del **Sistema de Generador de Constancias de Posgrado**xs
## Constancias
- **Generar constancias BEIFI** ✅
- **Generar constancias CONACYT** ✅

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
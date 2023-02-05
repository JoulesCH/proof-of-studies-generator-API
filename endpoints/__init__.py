from fastapi import APIRouter, Header, Depends
from fastapi.exceptions import HTTPException

import os

from . import  catalogs, home, letters_pdf, students_data, letters_zip


def apiKeyHeader(api_key: str = Header(..., description="The api key" )):
    if api_key != os.environ.get("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")

api_router = APIRouter(dependencies=[Depends(apiKeyHeader)])


api_router.include_router(home.router, tags=["Home"])

api_router.include_router(letters_pdf.router, tags=["Letter PDF Generator"], prefix="/letters/pdf")
api_router.include_router(letters_zip.router, tags=["Letters ZIP Generator"], prefix="/letters/zip")
api_router.include_router(students_data.router, tags=["Students Data"], prefix="/students")
api_router.include_router(catalogs.router, tags=["Catalogs"], prefix="/catalogs")

from fastapi import APIRouter
from . import  home, letters_pdf, students_data, letters_zip



api_router = APIRouter()

api_router.include_router(home.router, tags=["Home"])

api_router.include_router(letters_pdf.router, tags=["Letter PDF Generator"], prefix="/letters/pdf")
api_router.include_router(letters_zip.router, tags=["Letters ZIP Generator"], prefix="/letters/zip")
api_router.include_router(students_data.router, tags=["Students Data"], prefix="/students")

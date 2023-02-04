from fastapi import APIRouter
from . import beifi, conacyt, home, students_data



api_router = APIRouter()

api_router.include_router(home.router, tags=["Home"])

api_router.include_router(beifi.router, tags=["BEIFI"], prefix="/beifi")
api_router.include_router(conacyt.router, tags=["CONACYT"], prefix="/conacyt")
api_router.include_router(students_data.router, tags=["Students Data"], prefix="/students")

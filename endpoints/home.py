from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home():
    '''
    This is the home endpoint
    '''
    return {"message": "Hello World"}
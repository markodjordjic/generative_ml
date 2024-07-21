from fastapi import APIRouter

router = APIRouter()

@router.get("/read_request")
async def read_request():
    pass

@router.get("/get_response")
async def get_response():
    pass
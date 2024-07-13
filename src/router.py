from fastapi import APIRouter
from src.User.router import router as user_router

router = APIRouter()

router.include_router(user_router)

@router.get("/")
def read_root():
    return {"Hello": "World"}
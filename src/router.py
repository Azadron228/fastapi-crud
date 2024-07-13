from fastapi import APIRouter
from src.User.router import router as user_router
from src.Item.router import router as item_router

router = APIRouter()

router.include_router(user_router)
router.include_router(item_router, prefix="/items")

@router.get("/")
def read_root():
    return {"Hello": "World"}
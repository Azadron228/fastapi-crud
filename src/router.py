from fastapi import APIRouter

from src.User.router import router as user_router
from src.Item.router import router as item_router
from src.Order.router import router as order_router
from src.OrderItem.router import router as order_item_router

router = APIRouter()

router.include_router(user_router, tags=["User Registration"])
router.include_router(item_router, prefix="/items", tags=["Items CRUD"])
router.include_router(order_router, prefix="/order", tags=["Orders CRUD"])
router.include_router(order_item_router, prefix="/order", tags=["Add items to orders"])


@router.get("/")
async def root():
    return {"Hello": "World"}
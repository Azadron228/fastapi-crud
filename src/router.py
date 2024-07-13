from fastapi import APIRouter
from src.User.router import router as user_router
from src.Item.router import router as item_router
from src.Order.router import router as order_router
from src.OrderItem.router import router as order_item_router

router = APIRouter()

router.include_router(user_router)
router.include_router(item_router, prefix="/items")
router.include_router(order_router, prefix="/order")
router.include_router(order_item_router, prefix="/order")

@router.get("/")
def read_root():
    return {"Hello": "World"}
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.Order import crud as order_crud
from src.Order.model import OrderStatus
from src.Order.schemas import OrderCreate, OrderUpdate
from src.User.model import User
from src.auth.auth import get_current_user
from src.database import get_db

router = APIRouter()


@router.post("/")
async def create_order(order_form: OrderCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await order_crud.create_order(order_form,current_user.id, db)
    return {"message": "Order created successfully"}

@router.get("/")
async def get_all_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role.value == "admin":
        result = await order_crud.get_all_orders(db)
    else:
        result = await order_crud.get_all_orders(db)
    return result

@router.get("/{order_id}")
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = await order_crud.get_order_by_id(order_id, db)

    if current_user.role.value == "admin":
        return order
    elif current_user.id == order.user_id:
        return order
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@router.put("/{order_id}")
async def update_user(order_id:int, update_form: OrderUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = await order_crud.get_order_by_id(order_id, db)

    if current_user.role.value == "admin":
        result = await order_crud.update_order(update_form, order_id, db)
        return {"message": "Order updated successfully"}
    if current_user.id != order.user_id:
        result = await order_crud.update_order(update_form, order_id, db)
        return {"message": "Order updated successfully"}

    raise HTTPException(status_code=403, detail="Not enough permissions")



@router.delete("/{order_id}")
async def update_user(order_id:int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = await order_crud.get_order_by_id(order_id, db)
    if current_user.role.value == "admin":
        result = await order_crud.delete_order(order_id, db)
        return {"status": "successfully deleted"}
    elif current_user.id == order.user_id:
        canceled_order = OrderUpdate(
            id=order_id,
            status=OrderStatus.cancelled.value,
        )
        result = await order_crud.update_order(canceled_order, db)
        return {"status": "Order successfully canceled"}
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

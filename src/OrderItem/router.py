from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user

from src.OrderItem import crud as order_item_crud
from src.User.model import User
from src.auth.auth import get_current_user
from src.database import get_db

router = APIRouter()

@router.post("/{order_id}/{item_id}")
async def add_item_to_order(order_id:int, item_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role.value == "admin":
        result = await order_item_crud.add_item_to_order(item_id, order_id, db)
        return {"status": "ok", "order_id": order_id, "item_id": item_id}
    elif current_user.id != order_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    else:
        result = await order_item_crud.add_item_to_order(item_id, order_id, db)
        return {"status": "ok", "order_id": order_id, "item_id": item_id}

@router.delete("/{order_id}/{item_id}")
async def delete_item_from_order(order_id:int, item_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role.value == "admin":
        result = await order_item_crud.delete_item_from_order(item_id, order_id, db)
        return {"status": "ok", "order_id": order_id, "item_id": item_id}
    if current_user.id != order_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    else:
        result = await order_item_crud.delete_item_from_order(item_id, order_id, db)
        return {"status": "ok", "order_id": order_id, "item_id": item_id}
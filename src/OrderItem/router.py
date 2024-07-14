from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.OrderItem import crud as order_item_crud
from src.database import get_db

router = APIRouter()

@router.post("/{order_id}/{item_id}")
async def add_item_to_order(order_id:int, item_id: int, db: AsyncSession = Depends(get_db)):
    result = await order_item_crud.add_item_to_order(item_id, order_id, db)
    return result

@router.delete("/{order_id}/{item_id}")
async def delete_item_from_order(order_id:int, item_id: int, db: AsyncSession = Depends(get_db)):
    result = await order_item_crud.delete_item_from_order(item_id, order_id, db)
    return result
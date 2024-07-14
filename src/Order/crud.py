import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from select import select
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.Order.model import Order, OrderStatus
from src.Order.schemas import OrderUpdate, OrderCreate
from src.database import get_db





async def create_order(order: OrderCreate, session: AsyncSession):
    async with session:
        result = await session.execute(
            insert(Order).values(
                user_id = order.user_id,
                status = OrderStatus.pending,
                created_at = datetime.now(),
                updated_at = datetime.now(),
            )
        )
        await session.commit()
    return result

async def get_all_orders() -> Optional[Order]:
    async with get_db() as session:
        result = await session.execute(
            select(Order)
        )
    return result

async def get_all_orders_of_user(user_id) -> Optional[Order]:
    async with get_db() as session:
        result = await session.execute(
            select(Order).where(Order.user_id == user_id)
        )
    return result


async def get_order(id) -> Optional[Order]:
    async with get_db() as session:
        result = await session.execute(
            select(Order).where(Order.id == id)
        )
    return result


async def update_order(OrderUpdate: OrderUpdate) -> Order:
    async with get_db() as session:
        result = await session.execute(
            update(Order)
            .where(Order.id == OrderUpdate.id)
            .values(Order=OrderUpdate)
        )
    return result

async def delete_order(id: int):
    async with get_db() as session:
        result = await session.execute(
            delete(Order).where(Order.id == id)
        )
    return result


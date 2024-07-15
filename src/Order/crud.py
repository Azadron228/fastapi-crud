from datetime import datetime
from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.Order.model import Order, OrderStatus
from src.Order.schemas import OrderUpdate, OrderCreate
from src.database import get_db





async def create_order(order: OrderCreate, user_id: int, session: AsyncSession):
    async with session:
        result = await session.execute(
            insert(Order).values(
                user_id = user_id,
                status = OrderStatus.pending,
                created_at = datetime.now(),
                updated_at = datetime.now(),
            )
        )
        await session.commit()
    return result

async def get_all_orders(session: AsyncSession):
    async with session:
        result = await session.execute(select(Order))
        orders = result.scalars().all()
    return orders


async def get_all_orders_of_user(user_id) -> Optional[Order]:
    async with get_db() as session:
        result = await session.execute(
            select(Order).where(Order.user_id == user_id)
        )
    return result


async def get_order_by_id(id: int, session: AsyncSession):
    async with session:
        result = await session.execute(
            select(Order).where(Order.id == id))
        order = result.scalars().first()
    return order

async def update_order(order_update: OrderUpdate,order_id: int , session: AsyncSession):
    print("JOHUBYVGCTCRYGUHOIKJICFVGYUHDWITYFAUA", order_update.status)
    async with session:
        result = await session.execute(
            update(Order)
            .where(Order.id == order_id)
            .values(
                status = order_update.status,
                updated_at = datetime.now(),
            )
        )
        await session.commit()
        order = result
    return order

async def delete_order(order_id: int, session: AsyncSession):
    async with session:
        result = await session.execute(
            delete(Order).where(Order.id == order_id)
        )
        await session.commit()

    return result



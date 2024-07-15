from datetime import datetime

from fastapi import Depends
from select import select
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.Order.model import OrderStatus, Order
from src.Order.schemas import OrderCreate, OrderUpdate
from src.database import get_db


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, order: OrderCreate, user_id: int):
        async with self.session as session:
            result = await session.execute(
                insert(Order).values(
                    user_id=user_id,
                    status=OrderStatus.pending,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
            )
            await session.commit()
        return result

    async def get_all(
        self,
        limit: int = 25,
        offset: int = 0,
    ):
        async with self.session as session:
            result = await session.execute(select(Order).limit(limit).offset(offset))
            orders = result.scalars().all()
        return orders

    async def get_all_by_user_id(
        self,
        user_id: int,
        limit: int = 25,
        offset: int = 0,
    ):
        async with self.session as session:
            result = await session.execute(
                select(Order)
                .where(Order.user_id == user_id)
                .limit(limit)
                .offset(offset)
            )
            orders = result.scalars().all()
        return orders

    async def get_by_id(self, id: int):
        async with self.session as session:
            result = await session.execute(select(Order).where(Order.id == id))
            order = result.scalars().first()
        return order

    async def update(self, order_update: OrderUpdate, order_id: int):
        async with self.session as session:
            result = await session.execute(
                update(Order)
                .where(Order.id == order_id)
                .values(
                    status=order_update.status,
                    updated_at=datetime.now(),
                )
            )
            await session.commit()
            order = result
        return order

    async def delete(self, order_id: int):
        async with self.session as session:
            result = await session.execute(delete(Order).where(Order.id == order_id))
            await session.commit()

        return result


def get_order_service(session: AsyncSession = Depends(get_db)):
    return OrderService(session)

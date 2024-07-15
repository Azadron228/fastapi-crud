from fastapi import Depends
from sqlalchemy import select, func, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.OrderItem.model import OrderItem
from src.database import get_db


class OrderItemService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_item_to_order(self, item_id: int, order_id):
        async with self.session as session:
            result = await session.execute(
                select(func.count(OrderItem.id)).where(OrderItem.order_id == order_id)
            )
            item_count = result.scalar()
            result = await session.execute(
                insert(OrderItem)
                .values(
                    order_id=order_id,
                    item_id=item_id,
                    quantity=item_count + 1,
                )
            )
            await session.commit()
        return result

    async def delete_item_from_order(self, item_id: int, order_id):
        async with self.session as session:
            result = await session.execute(
                delete(OrderItem)
                .where(
                    item_id == item_id,
                    order_id == order_id,
                )
            )
            await session.commit()

        return result

def get_order_item_service(session: AsyncSession = Depends(get_db)):
    return OrderItemService(session)
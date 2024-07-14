from sqlalchemy import delete, insert

from src.OrderItem.model import OrderItem
from src.database import get_db


async def add_item_to_order(OrderItemAdd):
    async with get_db() as session:
        result = await session.execute(
            insert(OrderItem).values(OrderItemAdd)
        )
        items = result.scalars().all()
    return

async def delete_item_from_order(OrderItemDelete):
    async with get_db() as session:
        result = await session.execute(
            delete(OrderItem).where()
        )
        items = result.scalars().all()
    return
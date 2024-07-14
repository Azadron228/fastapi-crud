from pydantic import BaseModel
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.OrderItem.model import OrderItem
from src.database import get_db

class OrderItemAdd(BaseModel):
    id: int
    order_id: int
    item_id: int
    quantity: int


async def add_item_to_order(item_id: int , order_id , session: AsyncSession):
    async with session:
        result = await session.execute(
            insert(OrderItem)
            .values(
                order_id=order_id,
                item_id=item_id,
                quantity=911,
            )
        )
        await session.commit()
    return result

async def delete_item_from_order(item_id: int, order_id, session: AsyncSession):
    async with session:
        result = await session.execute(
            delete(OrderItem)
            .where(
    item_id == item_id,
                order_id == order_id,
            )
        )
        await session.commit()

    return result


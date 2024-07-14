from sqlalchemy import insert

from src.Order.model import Order
from src.database import get_db


async def create_order(OrderCreate):
    async with get_db() as session:
        result = await session.execute(
            insert(Order).values(OrderCreate)
        )

    return

async def get_all_orders(id):
    async with get_db() as session:
        result = await session.execute(
            select(Order)
        )
        items = result.scalars().all()
    return


def get_order(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return


def update_order(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return

def delete_order(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return


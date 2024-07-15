from datetime import datetime

from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.Item.model import Item
from src.Item.schemas import ItemCreate, ItemUpdate



async def create_item(item: ItemCreate,user_id: int, session: AsyncSession):
    async with session:
        result = await session.execute(
            insert(Item).values(
                name=item.name,
                description=item.description,
                owner_id=user_id,
                price=item.price,
                created_at=datetime.now(),
            )
        )
        await session.commit()
    return result

async def get_all_items(session: AsyncSession):
    async with session:
        result = await session.execute(select(Item))
        items = result.scalars().all()
    return items


async def get_item_by_id(id: int, session: AsyncSession):
    async with session:
        result = await session.execute(
            select(Item).where(Item.id == id))
        item = result.scalars().first()
    return item


async def update_item(item_id: int ,item_update: ItemUpdate, session: AsyncSession):
    async with session:
        result = await session.execute(
            update(Item)
            .where(Item.id == item_id)
            .values(
                name = item_update.name,
                description = item_update.description,
                price = item_update.price,
                created_at = datetime.now()
            )
        )
        await session.commit()
        item = result
    return item

async def delete_item(item_id: int, session: AsyncSession):
    async with session:
        result = await session.execute(
            delete(Item).where(Item.id ==item_id)
        )
        await session.commit()

    return result





from fastapi import Depends
from datetime import datetime

from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import user

from src.Item.model import Item
from src.Item.schemas import ItemCreate, ItemUpdate

from src.User.service import UserService
from src.database import get_db


class ItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        item: ItemCreate,
        user_id: int
    ):
        async with self.session as session:
            new_item = Item(
                name=item.name,
                description=item.description,
                owner_id=user_id,
                price=item.price,
                created_at=datetime.now()
            )

            session.add(new_item)
            await session.commit()
            await session.refresh(new_item)
        return new_item

    async def get_all(self, limit: int = 25, offset: int = 0):
        async with self.session as session:
            result = await session.execute(select(Item).limit(limit).offset(offset))
            items = result.scalars().all()
        return items

    async def get_by_id(self, id: int):
        async with self.session as session:
            result = await session.execute(select(Item).where(Item.id == id))
            item = result.scalars().first()
        return item

    async def update(self, item_id: int, item_update: ItemUpdate):
        async with self.session as session:
            result = await session.execute(
                update(Item)
                .where(Item.id == item_id)
                .values(
                    name=item_update.name,
                    description=item_update.description,
                    price=item_update.price,
                    created_at=datetime.now(),
                )
            )
            await session.commit()
            item = result
        return item

    async def delete(self, item_id: int):
        async with self.session as session:
            result = await session.execute(delete(Item).where(Item.id == item_id))
            await session.commit()

        return result


def get_item_service(session: AsyncSession = Depends(get_db)):
    return ItemService(session)

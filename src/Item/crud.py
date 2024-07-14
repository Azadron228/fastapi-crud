from sqlalchemy import select, insert, update, delete

from src.Item.model import Item
from src.Item.schemas import ItemUpdate, ItemCreate
from src.database import get_db

class ItemCreate(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    price: float
    created_at: datetime


class ItemUpdate(BaseModel):
    name: str
    description: str
    owner_id: int
    price: float
    created_at: datetime
async def create_item(create_item: ItemCreate) -> Item:
    async with get_db() as session:
        result = await session.execute(
            insert(Item).values(create_item)
        )

    return result

async def get_all_items():
    async with get_db() as session:
        result = await session.execute(
            select(Item)
        )
        items = result.scalars().all()
    return items

async def get_item(id):
    async with get_db() as session:
        result = await session.execute(
            select(Item).where(Item.id == id)
        )
        item = result.scalars().all()
    return item

async def update_item(item_update: ItemUpdate):
    async with get_db() as session:
        result = await session.execute(
            update(Item).values(item_update)
        )

    return result

async def delete_item(id):
    async with get_db() as session:
        result = await session.execute(
            delete(Item).where(Item.id == id)
        )
    return result


import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime, select, insert, update, delete

# Assuming Item is defined with appropriate fields and relationships
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, index=True)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class ItemCreate(BaseModel):
    name: str
    description: str
    owner_id: int
    price: float


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None
    price: Optional[float] = None


async def create_item(create_item: ItemCreate) -> Item:
    item = Item(**create_item.dict())
    async with get_db() as session:
        session.add(item)
        await session.commit()
        await session.refresh(item)
    return item


async def get_all_items():
    async with get_db() as session:
        result = await session.execute(select(Item))
        items = result.scalars().all()
    return items


async def get_item(id: int) -> Optional[Item]:
    async with get_db() as session:
        result = await session.execute(select(Item).where(Item.id == id))
        item = result.scalars().first()
    return item


async def update_item(id: int, item_update: ItemUpdate) -> bool:
    async with get_db() as session:
        stmt = update(Item).where(Item.id == id).values(item_update.dict(exclude_unset=True))
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0


async def delete_item(id: int) -> bool:
    async with get_db() as session:
        stmt = delete(Item).where(Item.id == id)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0




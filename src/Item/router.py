from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import crud

from src.Item.model import Item
from src.Item.schemas import ItemCreate
from src.auth.auth import auth_wrapper
from src.database import get_db

router = APIRouter()

@router.get("/")
async def get_items(user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()

    return items

@router.get("/{item_id}")
async def get_item_by_id(item_id: int, user=Depends(auth_wrapper), db: Session = Depends(get_db)):
    async with db as session:
        result = await session.execute(
            select(Item).where(
                Item.id == item_id,
                            Item.owner_id == user["user_id"]
            )
        )

        item = result.scalars().first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/")
async def create_item(item: ItemCreate, user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    stmt = (
        insert(Item).
        values(name=item.name,
               description=item.description,
               owner_id = user["user_id"],
               price=item.price,
               created_at=item.created_at
               )
    )

    result = await db.execute(stmt)
    await db.commit()

    return result

@router.put("/")
async def update_item(item: ItemCreate, user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    stmt = (
        insert(Item).
        values(name=item.name,
               description=item.description,
               owner_id = user["user_id"],
               price=item.price,
               created_at=item.created_at
               )
    )

    result = await db.execute(stmt)
    await db.commit()

    return result

@router.delete("/")
async def delete_item(item: ItemCreate, user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    stmt = (
        insert(Item).
        values(name=item.name,
               description=item.description,
               owner_id = user["user_id"],
               price=item.price,
               created_at=item.created_at
               )
    )

    result = await db.execute(stmt)
    await db.commit()

    return result
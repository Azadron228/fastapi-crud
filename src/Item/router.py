from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.Item import crud as item_crud
from src.Item.schemas import ItemCreate, ItemUpdate
from src.User.model import User
from src.auth.auth import get_current_user

from src.database import get_db

router = APIRouter()

@router.post("/")
async def create_item(item_form: ItemCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    result = await item_crud.create_item(item_form,current_user.id, db)
    return {"message": "Item created successfully"}


@router.get("/")
async def get_all_items(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    result = await item_crud.get_all_items(db)
    return result


@router.get("/{item_id}")
async def get_item_by_id(item_id: int,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    result = await item_crud.get_item_by_id(item_id, db)
    return result

@router.put("/{item_id}")
async def update_item(item_id: int, update_form: ItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    result = await item_crud.update_item(item_id, update_form, db)

    return {"message": "Item updated successfully"}

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    result = await item_crud.delete_item(item_id, db)
    return {"message": "Item deleted successfully"}


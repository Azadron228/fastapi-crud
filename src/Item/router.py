from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from src.Item import crud
from src.Item.schemas import ItemCreate
from src.auth.auth import auth_wrapper, user_is_admin
from src.database import get_db

router = APIRouter()

@router.post("/")
async def create_item(item_form: ItemCreate, user=Depends(auth_wrapper), db: Session = Depends(get_db)):
    if user_is_admin:
        result = crud.create_item(item_form)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return result

@router.get("/")
async def get_all_items(user=Depends(auth_wrapper), db: Session = Depends(get_db)):
    if user_is_admin:
        result = crud.get_all_items()
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return result


@router.get("/{item_id}")
async def get_item_by_id(item_id: int, user=Depends(auth_wrapper), db: Session = Depends(get_db)):
    if user_is_admin:
        result = crud.get_item(item_id)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return result



@router.put("/{item_id}")
async def update_item(item_id: int, update_form: UpdateItem):
    if user_is_admin:
        result = crud.update_item(item_id, update_form)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return result

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    if user_is_admin:
        result = crud.delete_item(item_id)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return result
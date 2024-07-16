from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends
from src.Item.schemas import ItemCreate, ItemUpdate, ItemDetails
from src.Item.service import get_item_service, ItemService
from src.User.model import User
from src.auth.auth import get_current_user, is_admin

router = APIRouter()

@router.post("/", response_model=ItemDetails)
async def create_item(
    item_form: ItemCreate,
    current_user: User = Depends(get_current_user),
    item_service: ItemService = Depends(get_item_service),
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    result = await item_service.create(item_form, current_user.id)
    item = ItemDetails(
        id=result.id,
        name=result.name,
        description = result.description,
        owner_id = result.owner_id,
        price = result.price,
    )

    return item


@router.get("/", response_model=List[ItemDetails])
async def get_all_items(
    limit: int = 25,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    user_service: ItemService = Depends(get_item_service),
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    result = await user_service.get_all(limit, offset)
    return result


@router.get("/{item_id}", response_model=ItemDetails)
async def get_item_by_id(
    item_id: int,
    current_user: User = Depends(get_current_user),
    user_service: ItemService = Depends(get_item_service),
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    result = await user_service.get_by_id(item_id)
    return result


@router.put("/{item_id}")
async def update_item(
    item_id: int,
    update_form: ItemUpdate,
    current_user: User = Depends(get_current_user),
    user_service: ItemService = Depends(get_item_service),
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await user_service.update(item_id, update_form)

    return {"message": "Item updated successfully"}


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    user_service: ItemService = Depends(get_item_service),
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await user_service.delete(item_id)
    return {"message": "Item deleted successfully"}

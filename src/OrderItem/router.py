from fastapi import APIRouter, HTTPException, Depends
from src.OrderItem.model import OrderItem
from src.OrderItem.service import get_order_item_service
from src.User.model import User
from src.auth.auth import get_current_user, is_admin

router = APIRouter()


@router.post("/{order_id}/{item_id}")
async def add_item_to_order(
    order_id: int,
    item_id: int,
    current_user: User = Depends(get_current_user),
    order_item_service: OrderItem = Depends(get_order_item_service),
):

    if is_admin(current_user) or current_user.id == order_id:
        await order_item_service.add_item_to_order(item_id, order_id)
        return {"status": "ok", "order_id": order_id, "item_id": item_id}

    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")


@router.delete("/{order_id}/{item_id}")
async def delete_item_from_order(
    order_id: int,
    item_id: int,
    current_user: User = Depends(get_current_user),
    order_item_service: OrderItem = Depends(get_order_item_service),
):

    if is_admin(current_user) or current_user.id == order_id:
        await order_item_service.delete_item_from_order(item_id, order_id)
        return {"status": "ok", "order_id": order_id, "item_id": item_id}

    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

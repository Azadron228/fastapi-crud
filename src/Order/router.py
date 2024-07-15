from fastapi import APIRouter, HTTPException, Depends
from src.Order.model import OrderStatus
from src.Order.schemas import OrderCreate, OrderUpdate
from src.Order.service import OrderService, get_order_service
from src.User.model import User
from src.auth.auth import get_current_user, is_admin

router = APIRouter()


@router.post("/")
async def create_order(
    order_form: OrderCreate,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
):
    await order_service.create(order_form, current_user.id)
    return {"message": "Order created successfully"}


@router.get("/")
async def get_all_orders(
    limit: int = 25,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
):
    if is_admin(current_user):
        result = await order_service.get_all(limit, offset)
    else:
        result = await order_service.get_all_by_user_id(current_user.id, limit, offset)
    return result


@router.get("/{order_id}")
async def get_order_by_id(
    order_id: int,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.get_by_id(order_id)

    if is_admin(current_user):
        return order
    elif current_user.id == order.user_id:
        return order
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")


@router.put("/{order_id}")
async def update_order(
    order_id: int,
    update_form: OrderUpdate,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.get_by_id(order_id)

    if is_admin(current_user):
        await order_service.update(update_form, order_id)
        return {"message": "Order updated successfully"}
    if current_user.id != order.user_id:
        await order_service.update(update_form, order_id)
        return {"message": "Order updated successfully"}

    raise HTTPException(status_code=403, detail="Not enough permissions")


@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.get_by_id(order_id)
    if is_admin(current_user):
        await order_service.delete(order_id)
        return {"status": "successfully deleted"}
    elif current_user.id == order.user_id:
        canceled_order = OrderUpdate(
            id=order_id,
            status=OrderStatus.cancelled.value,
        )
        await order_service.update(canceled_order)
        return {"status": "Order successfully canceled"}
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

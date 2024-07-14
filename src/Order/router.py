from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.Order import crud as order_crud
from src.Order.schemas import OrderCreate, OrderUpdate
from src.database import get_db

# from src.auth.auth import user_is_admin

router = APIRouter()


@router.post("/")
async def create_order(order_form: OrderCreate, db: AsyncSession = Depends(get_db)):

    result = await order_crud.create_order(order_form, db)


    return result

@router.get("/")
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    result = await order_crud.get_all_orders(db)
    return result

@router.get("/{order_id}")
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await order_crud.get_order_by_id(order_id, db)
    return result

@router.put("/{order_id}")
async def update_user(order_id:int, update_form: OrderUpdate, db: AsyncSession = Depends(get_db)):
    # if user_is_admin:
    result = await order_crud.update_order(order_id, update_form, db)
    return result

@router.delete("/{order_id}")
async def update_user(order_id:int, db: AsyncSession = Depends(get_db)):
    result = await order_crud.delete_order(order_id, db)
    return result


# @router.post("/")
# async def create_order(user=Depends(auth_wrapper), db: Session = Depends(get_db)):
#     if user:
#         result = crud.create_order(db, user)
#     else:
#         raise HTTPException()
#     return {"message": "Order created successfully"}


# @router.post("/")
# async def get_all_orders(user=Depends(auth_wrapper), db: Session = Depends(get_db)):
#
#     orders = crud.get_all_orders(db)
#     return orders
#
# @router.post("/{order_id}")
# async def get_order(order_id:str, user=Depends(auth_wrapper), db: Session = Depends(get_db)):
#     if user:
#         order = crud.get_order(order_id)
#     else:
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return order
#
# @router.put("/{order_id}")
# async def update_order(order_id:str, update_form: OrderUpdate, user=Depends(auth_wrapper), db: Session = Depends(get_db)):
#     if user:
#         order = crud.update_order(order_id, update_form)
#     else:
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return order
#
#
#     return items
#
# @router.delete("/{order_id}")
# async def delete_order(order_id:str, user=Depends(auth_wrapper), db: Session = Depends(get_db)):
#     if user:
#         order = crud.delete_order(order_id)
#     else if user_is_admin(user):
#         order = crud.cancel_order(order_id)
#     else:
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return order

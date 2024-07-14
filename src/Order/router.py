from fastapi import APIRouter, HTTPException

from src.Order import crud
from src.auth.auth import user_is_admin

router = APIRouter()

@router.post("/")
async def create_order(user=Depends(auth_wrapper), db: Session = Depends(get_db)):
    if user:
        result = crud.create_order(db, user)
    else:
        raise HTTPException()
    return {"message": "Order created successfully"}


@router.post("/")
async def get_all_orders(user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    orders = crud.get_all_orders(db)
    return orders

@router.post("/{order_id}")
async def get_order(order_id:str, user=Depends(auth_wrapper), db: Session = Depends(get_db)):
    if user:
        order = crud.get_order(order_id)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return order

@router.put("/{order_id}")
async def update_order(order_id:str, update_form: OrderUpdate, user=Depends(auth_wrapper), db: Session = Depends(get_db)):
    if user:
        order = crud.update_order(order_id, update_form)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return order


    return items

@router.delete("/{order_id}")
async def delete_order(order_id:str, user=Depends(auth_wrapper), db: Session = Depends(get_db)):
    if user:
        order = crud.delete_order(order_id)
    else if user_is_admin(user):
        order = crud.cancel_order(order_id)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return order

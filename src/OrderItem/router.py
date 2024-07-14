from fastapi import APIRouter, HTTPException

from src.OrderItem import crud

router = APIRouter()

@router.post("/{order_id}/{item_id}")
async def add_item_to_order(user=Depends(auth_wrapper), db: Session = Depends(get_db)):
    if user:
        result = crud.add_item_to_order()
    else:
        raise HTTPException()
    return result


@router.delete("/{order_id/{item_id}")
async def delete_item_from_order(order_id: str, item_id: str user=Depends(auth_wrapper), db: Session = Depends(get_db)):
    if user:
        result = crud.delete_item_from_order(order_id, item_id)
    else:
        raise HTTPException()
    return result

from pydantic import BaseModel


class OrderItemAdd(BaseModel):
    id: int
    order_id: int
    item_id: int
    quantity: int
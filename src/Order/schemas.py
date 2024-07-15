from datetime import datetime

from pydantic import BaseModel

from src.Order.model import OrderStatus

class OrderSchema(BaseModel):
    status: OrderStatus

class OrderDetails(OrderSchema):
    id: int
    user_id: int
class OrderCreate(OrderSchema):
    pass

class OrderUpdate(OrderSchema):
    status: OrderStatus
    created_at: datetime
    updated_at: datetime




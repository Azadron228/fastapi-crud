import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.Order.model import OrderStatus

class OrderCreate(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    created_at: datetime

class OrderUpdate(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    status: Optional[OrderStatus]
    created_at: Optional[datetime]




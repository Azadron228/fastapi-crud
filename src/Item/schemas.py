from datetime import datetime

from pydantic import BaseModel


class ItemCreate(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    price: float
    created_at: datetime
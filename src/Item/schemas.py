from typing import Optional
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str
    owner_id: int
    price: float

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None
    price: Optional[float] = None

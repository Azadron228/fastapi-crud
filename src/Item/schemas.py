import datetime

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: float

class ItemDetails(BaseModel):
    id:int
    name: str
    description: str
    owner_id: int
    price: float


class ItemCreate(Item):
    pass


class ItemUpdate(Item):
    pass

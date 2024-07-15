from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: float


class ItemCreate(Item):
    pass


class ItemUpdate(Item):
    pass

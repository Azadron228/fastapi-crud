from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    name: str
    email: str
    password: str


class AuthCredentials(BaseModel):
    email: str
    password: str
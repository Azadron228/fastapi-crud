from datetime import datetime

from pydantic import BaseModel

from src.User.model import UserRole


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class AuthCredentials(BaseModel):
    email: str
    password: str
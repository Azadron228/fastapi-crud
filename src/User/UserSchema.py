from datetime import datetime

from pydantic import BaseModel

from src.models import UserRole


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: UserRole

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole

class AuthCredentials(BaseModel):
    email: str
    password: str
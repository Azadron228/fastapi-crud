from pydantic import BaseModel, ConfigDict

from src.User.model import UserRole


class UserDetails(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str



class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole = UserRole.user

class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole = UserRole.admin


class UserUpdate(BaseModel):
    name: str
    email: str
    password: str


class AuthCredentials(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str

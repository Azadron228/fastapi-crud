from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi import APIRouter
from pydantic import BaseModel

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from src.Item.model import Item
from src.User.UserSchema import AuthCredentials, UserCreate, UserSchema
from src.User.model import User
from src.auth.auth import auth_wrapper

from src.auth.jwt import encode_token, verify_password
from src.config import settings

from src.database import get_db

router = APIRouter()

# auth_handler = AuthHandler()
# users = []

class LoginRequest(BaseModel):
    email: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    stmt = (
        insert(User).
        values(name=user.name, email=user.email, password=user.password)
    )
    result = await db.execute(stmt)
    await db.commit()

    return result

@router.post("/token")
async def get_token(login_request: LoginRequest, db: Session = Depends(get_db)):
    res = await db.execute(
        select(User)
        .where(
            User.email == login_request.email
        )
    )
    user = res.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = {
        "user_id": user.id,
        "email": user.email
    }

    access_token = encode_token(token_data, settings.TOKEN_SECRET)
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(auth_wrapper)]):
    return current_user

@router.get('/unprotected')
def unprotected():
    return {'hello': 'world'}


@router.get('/protected')
def protected(username=Depends(auth_wrapper)):
    return {'name': username}



from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.handlers.bcrypt import bcrypt

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from src.User.UserSchema import UserCreate
from src.User.model import User
from src.auth.auth import auth_wrapper

from src.auth.jwt import encode_token, hash_password
from src.auth.schemas import Token
from src.config import settings

from src.database import get_db

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    stmt = (
        insert(User).
        values(name=user.name, email=user.email, password=hashed_password)
    )
    result = await db.execute(stmt)
    await db.commit()

    return result


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    res = await db.execute(
        select(User)
        .where(
            User.email == form_data.username
        )
    )

    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


    if not bcrypt.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

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



from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.handlers.bcrypt import bcrypt

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.Item.schemas import ItemCreate
from src.Order.schemas import OrderCreate

from src.Item import crud as item_crud
from src.Order import crud as order_crud
from src.User import crud
from src.User.crud import create_user
from src.User.schemas import UserCreate, UserUpdate
from src.User.model import User
from src.auth.auth import auth_wrapper

from src.auth.jwt import encode_token, hash_password
from src.auth.schemas import Token, TokenData
from src.config import settings

from src.database import get_db

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(
            insert(User).values(
                name=user.name,
                email=user.email,
                password=user.password
            )
        )
        await session.commit()
    # created_user = await create_user(db, user)
    return result

@router.get("/users")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    # if user_is_admin:
    result = await crud.get_all_users(db)
    return result

@router.get("/users/{uesr_id}")
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_user_by_id(user_id, db)
    return result

@router.put("/users/{user_id}")
async def update_user(user_id:int, update_form: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await crud.update_user(user_id, update_form, db)
    return result


@router.delete("/users/{user_id}")
async def update_user(user_id:int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_user(user_id, db)
    return result

@router.post("/token", tags=["Authorization"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):

    user = await crud.get_user_by_email(form_data.username, db)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not bcrypt.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token_data = TokenData(email=user.email)

    access_token = encode_token(token_data, settings.TOKEN_SECRET)
    return Token(access_token=access_token, token_type="bearer")
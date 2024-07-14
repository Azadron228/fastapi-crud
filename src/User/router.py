from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.handlers.bcrypt import bcrypt

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from src.User import crud
from src.User.schemas import UserCreate
from src.User.model import User
from src.auth.auth import auth_wrapper, user_is_admin

from src.auth.jwt import encode_token, hash_password
from src.auth.schemas import Token, TokenData
from src.config import settings

from src.database import get_db

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    result = crud.create_user(user)
    return result

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):

    user = crud.get_user_by_email()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not bcrypt.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token_data = TokenData(email=user.email)

    access_token = encode_token(token_data, settings.TOKEN_SECRET)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    if user_is_admin:
        result = crud.get_all_users()
    return result

@router.get("/users/{uesr_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    result = crud.get_user_by_id(user_id)
    return result

@router.put("/users/{user_id}")
async def update_user(user_id:int, update_form: UserUpdate, db: Session = Depends(get_db)):
    if user_is_admin:
        result = crud.update_user(user_id, update_form)
    return result

@router.delete("/users/{user_id}")
async def update_user(user_id:int, update_form: UserUpdate, db: Session = Depends(get_db)):
    if user_is_admin:
        result = crud.delete_user(user_id)
    return result



























# @router.get("/users/me/")
# async def read_users_me(
#     current_user: Annotated[User, Depends(auth_wrapper)]):
#     return current_user






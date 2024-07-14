from typing import Annotated, List

from fastapi import Depends, HTTPException, Security
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from src.User import crud

from src.User.schemas import UserCreate, UserUpdate
from src.User.model import User
from src.auth.auth import get_current_user

from src.auth.jwt import create_access_token, verify_password
from src.auth.schemas import Token

from src.database import get_db

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await crud.create_user(user,db)
    return {"message": "User created successfully"}

@router.get("/users")
async def get_all_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = await crud.get_all_users(db)
    return users

@router.get("/users/{uesr_id}")
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    result = await crud.get_user_by_id(user_id, db)
    return result

@router.put("/users/{user_id}")
async def update_user(user_id:int, update_form: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    result = await crud.update_user(user_id, update_form, db)
    return result


@router.delete("/users/{user_id}")
async def update_user(user_id:int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        user = await crud.delete_user(user_id, db)
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@router.post("/token", tags=["Authorization"])
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):

    user = await crud.get_user_by_email(form_data.username, db)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    data = {
        "sub": user.id,
        "user_id": user.id,
        "email": user.email,
        "scopes": user.role.value
    }

    access_token = create_access_token(data)
    return Token(access_token=access_token, token_type="bearer")
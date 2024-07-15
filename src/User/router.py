from typing import Annotated, List

from fastapi import Depends, HTTPException
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from src.User.schemas import UserCreate, UserUpdate, UserDetails, UserResponse
from src.User.model import User
from src.User.service import UserService, get_user_service
from src.auth.auth import get_current_user, is_admin

from src.auth.auth import create_access_token, verify_password
from src.auth.schemas import Token


router = APIRouter()


@router.post("/register")
async def register_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    await user_service.create(user)
    return {"message": "User created successfully"}


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    limit: int = 25,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    if is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = await user_service.get_all(limit=limit, offset=offset)
    return users


@router.get("/users/{user_id}", response_model=UserDetails)
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    if not is_admin(current_user) and current_user.id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this user"
        )

    result = await user_service.get_by_id(user_id)
    return result


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    update_form: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    if not is_admin(current_user) and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await user_service.update(user_id, update_form)
    return {"message": "User updated successfully"}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    if not is_admin(current_user):
        await user_service.delete(user_id)
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")


@router.post("/token", tags=["Authorization"])
async def get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service),
):
    # form_data.user is email
    user = await user_service.get_by_email(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    data = {
        "sub": user.id,
        "user_id": user.id,
        "email": user.email,
    }

    access_token = create_access_token(data)
    return Token(access_token=access_token, token_type="bearer")

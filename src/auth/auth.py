from datetime import timedelta, datetime
from http.client import HTTPException
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.User.model import User
from src.User.service import UserService, get_user_service
from src.auth.schemas import TokenData
from src.config import settings

key = settings.TOKEN_SECRET
algorithm = settings.TOKEN_ALGORITHM



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def is_admin(user: User) -> bool:
    return user.role.value == "admin"


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserService = Depends(get_user_service),
):
    decode_token = await decode_access_token(token)
    user = await user_service.get_by_id(decode_token["user_id"])
    return user



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.TOKEN_SECRET, algorithm=settings.TOKEN_ALGORITHM
    )
    return encoded_jwt


async def decode_access_token(
    token: oauth2_scheme,
    key: str = settings.TOKEN_SECRET,
    algorithm: str = settings.TOKEN_ALGORITHM,
) -> TokenData:
    try:
        payload = jwt.decode(token, key, algorithm)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from src.auth.schemas import TokenData
from src.config import settings

key = settings.TOKEN_SECRET
algorithm = settings.TOKEN_ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.TOKEN_SECRET, algorithm=settings.TOKEN_ALGORITHM)
    return encoded_jwt

async def decode_access_token(token: str, key: str = settings.TOKEN_SECRET, algorithm: str = settings.TOKEN_ALGORITHM) -> TokenData :
    try:
        payload = jwt.decode(token, key, algorithm)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


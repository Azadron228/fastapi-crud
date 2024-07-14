from typing import Annotated, Optional

import jwt
from fastapi import Security, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.User import crud
from src.User.model import User
from src.auth.jwt import decode_token

from src.config import settings
from src.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def auth_wrapper(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_token(token, settings.TOKEN_SECRET)
    return payload

async def get_user_instance(db: Session = Depends(get_db), username: Optional[str] = None, email: Optional[str] = None
) -> Optional[User]:
    if username is not None:
        user = crud.get_user_by_username(db, username)
    elif email is not None:
        user = crud.get_user_by_email(db, email)
    else:
        return None
    return user

async def get_current_user_instance(
    token: Optional[str] = Depends(oauth2_scheme),
) -> User:
    if token is None:
        pass
    try:
        decode_token(token, settings.TOKEN_SECRET, settings.TOKEN_ALGORITHM)
    except JWTError:
        raise HTTPException()
    try:
        token_data: TokenData = payload.sub
    except jwt.error:
        raise HTTPException(status_code=400, detail="Token data invalid")

    user = await get_user_instance(db: Session = Depends(get_db), email=token_data.email)

    if user is None:
        raise CredentialsException()
    return user

async def user_is_admin(current_user: User = Depends(get_current_user_instance)):
    return

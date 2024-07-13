from typing import Annotated

from fastapi import Security, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials

from src.auth.jwt import decode_token
from src.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def auth_wrapper(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_token(token, settings.TOKEN_SECRET)
    return payload

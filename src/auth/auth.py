from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.User.service import UserService, get_user_service
from src.auth.jwt import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserService = Depends(get_user_service)
):
    decode_token = await decode_access_token(token)
    user = await user_service.get_by_id(decode_token["user_id"])
    return user

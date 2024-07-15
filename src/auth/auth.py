from typing import Optional, Annotated

from sqlalchemy.ext.asyncio import AsyncSession


from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.User import crud as user_crud
from src.User.model import User
from src.auth.jwt import decode_access_token
from src.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)) -> Optional[User]:
    decode_token = await decode_access_token(token)
    user = await user_crud.get_user_by_id(decode_token["user_id"],db)
    return user

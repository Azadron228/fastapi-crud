from fastapi import Depends
from src.database import get_db
from fastapi import HTTPException, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.User.model import User
from src.User.schemas import UserCreate, UserUpdate
from src.auth.jwt import password_hash

class UserService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreate) -> User:
        async with self.session as session:
            result = await session.execute(select(User).filter_by(email=user.email))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            user = await session.execute(
                insert(User).values(
                    name=user.name,
                    email=user.email,
                    password=password_hash(user.password),
                )
            )
            await session.commit()
        return user

    async def get_all(self):
        async with self.session as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
        return users

    async def get_by_email(self, email: str):
        async with self.session as session:
            result = await session.execute(
                select(User).where(User.email == email))
            user = result.scalars().first()
        return user

    async def get_by_id(self, id: int):
        async with self.session as session:
            result = await session.execute(
                select(User).where(User.id == id))
            user = result.scalars().first()
        return user

    async def update(self, user_id: int, user_update: UserUpdate):
        async with self.session as session:
            result = await session.execute(
                update(User)
                .where(User.id == user_id)
                .values(
                    name=user_update.name,
                    email=user_update.email,
                    password=user_update.password
                )
            )
            await session.commit()
            user = result
        return user

    async def delete(self, id: int,):
        async with self.session as session:
            result = await session.execute(
                delete(User).where(User.id == id)
            )
            await session.commit()

        return result

def get_user_service(session: AsyncSession = Depends(get_db)):
    return UserService(session)
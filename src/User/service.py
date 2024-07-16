from fastapi import Depends
from src.database import get_db
from fastapi import HTTPException, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.User.model import User
from src.User.schemas import UserCreate, UserUpdate, AdminCreate
from src.auth.utils import password_hash


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreate | AdminCreate) -> User:
        async with self.session as session:
            result = await session.execute(select(User).filter_by(email=user.email))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

            new_user = User(
                name=user.name,
                email=user.email,
                password=password_hash(user.password),
                role=user.role,
            )

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
        return new_user

    async def get_all(
        self,
        limit: int = 25,
        offset: int = 0,
    ):
        async with self.session as session:
            result = await session.execute(select(User).limit(limit).offset(offset))
            users = result.scalars().all()
        return users

    async def get_by_email(self, email: str):
        async with self.session as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
        return user

    async def get_by_id(self, id: int):
        async with self.session as session:
            result = await session.execute(select(User).where(User.id == id))
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
                    password=password_hash(user_update.password),
                )
            )
            await session.commit()
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
        return user

    async def delete(
        self,
        user_id: int,
    ):
        async with self.session as session:
            existing_user = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = existing_user.scalar_one_or_none()

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            await session.execute(delete(User).where(User.id == user_id))
            await session.commit()

        return user


def get_user_service(session: AsyncSession = Depends(get_db)):
    return UserService(session)

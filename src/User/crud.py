from sqlalchemy import select, insert, update, delete

from src.User.model import User
from src.User.schemas import UserCreate
from src.database import get_db


async def create_user(UserCreate: UserCreate):
    async with get_db() as session:
        result = await session.execute(
            insert(User).values(UserCreate)
        )
    return

async def get_all_users():
    async with get_db() as session:
        result = await session.execute(
            select(User)
        )
        users = result.scalars().all()
    return users

async def get_user_by_email(email: str):
    async with get_db() as session:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalars().first()
    return user

def update_user(UserUpdate: UserUpdate):
    async with get_db() as session:
        result = await session.execute(
            update(User)
        )

    return

async def delete_user(id):
    async with get_db() as session:
        result = await session.execute(
            delete(User).where(User.id == id)
        )

    return



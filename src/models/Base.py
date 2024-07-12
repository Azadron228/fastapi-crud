from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase

from src.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
class Base(DeclarativeBase):
    pass
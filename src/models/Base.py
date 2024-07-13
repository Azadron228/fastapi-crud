from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncConnection
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase

from src.config import settings

# engine = create_async_engine(settings.DATABASE_URL, echo=True)
# DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# class Base(DeclarativeBase):
#     pass

engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
)

Base = declarative_base()
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
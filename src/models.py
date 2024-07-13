import enum
from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import Enum, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import mapped_column, Mapped, Session, relationship

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncConnection
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase

from src.config import settings


class Base(DeclarativeBase):
    pass

engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserRole(enum.Enum):
    user = 'user'
    admin = 'admin'

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(45))
    email: Mapped[str] = mapped_column(String(45), unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    # role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)
    # items: Mapped[List["Item"]] = relationship("Item", back_populates="users")
    # items: Mapped[List["Item"]] = relationship("Item", back_populates="owner")
    item: Mapped[List["Item"]] = relationship(back_populates="user")


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=datetime.now)
    # owner: Mapped["User"] = relationship("User",back_populates="items")
    # owner: Mapped["User"] = relationship("User", back_populates="itmes")
    user: Mapped["User"] = relationship(back_populates="item")






#
# class OrderStatus(enum.Enum):
#     pending = 'pending'
#     completed = 'completed'
#     cancelled = 'cancelled'
#
# class Order(Base):
#     __tablename__ = 'orders'
#
#     id: Mapped[int] = mapped_column(index=True, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
#     status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=datetime.now)
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=datetime.now)
#
# class OrderItem(Base):
#     __tablename__ = 'order_items'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
#     user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
#     quantity: Mapped[int] = mapped_column(Integer)
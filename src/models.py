import enum
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import Enum, String
from sqlalchemy.orm import mapped_column, Mapped, Session, relationship

from src.auth.jwt import hash_password
from src.models.Base import Base

class UserRole(enum.Enum):
    user = 'user'
    admin = 'admin'

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(45))
    email: Mapped[str] = mapped_column(String(45), unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)
    items: Mapped[List["Item"]] = relationship("Item", back_populates="users")

def create_user(db: Session, name: str, email: str, password: str, role: UserRole):
    # existing_user = db.query(User).filter(User.email == email).first()
    # if existing_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email already registered"
    #     )
    print("Password is a " + password)
    # hashed_password = hash_password(password)
    user = User(name=name, email=email, password=password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=datetime.now)
    owner: Mapped["User"] = relationship("User",back_populates="items")
    ownerdwa: Mapped["User"] = relationship()
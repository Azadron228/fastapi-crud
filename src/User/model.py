import enum
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


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
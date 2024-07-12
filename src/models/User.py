import enum

from sqlalchemy import Enum, String
from sqlalchemy.orm import mapped_column, Mapped

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
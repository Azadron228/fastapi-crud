import enum
from datetime import datetime

from sqlalchemy import Enum, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.models.Base import Base


class OrderStatus(enum.Enum):
    pending = 'pending'
    completed = 'completed'
    cancelled = 'cancelled'

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(index=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=datetime.now)
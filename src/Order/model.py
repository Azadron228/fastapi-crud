import enum
from datetime import datetime

from sqlalchemy import Enum, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class OrderStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(index=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.pending
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now
    )

    user = relationship("User", back_populates="orders")
    order_item = relationship("OrderItem", back_populates="orders")

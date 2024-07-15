from datetime import datetime

from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now
    )

    order_item = relationship("OrderItem", back_populates="items")

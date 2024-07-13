from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class OrderItem(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped["Order"] = relationship(back_populates="order_items")
    item: Mapped["Item"] = relationship(back_populates="order_items")
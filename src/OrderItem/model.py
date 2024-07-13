from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped

from src.database import Base


class OrderItem(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer)
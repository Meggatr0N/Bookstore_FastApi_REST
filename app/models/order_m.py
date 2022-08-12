from sqlalchemy import (
    Integer,
    Boolean,
    Column,
    Date,
    ForeignKey,
    SmallInteger,
    DateTime,
    Numeric,
)
from datetime import datetime
from sqlalchemy.orm import relationship

from app.database.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    date_placed = Column(DateTime(), default=datetime.now)
    customer_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Numeric(10, 2))
    paid = Column(Boolean, default=False)
    delivery_date = Column(Date, default=None)
    complete = Column(Boolean, default=False)

    order_items = relationship("OrderItem", backref="order")

    def __repr__(self):
        return f"Order ID: {self.id}"


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey("orders.id"))
    book_id = Column(Integer(), ForeignKey("books.id"))
    quantity = Column(SmallInteger(), nullable=False)
    book = relationship("Book")

    def __repr__(self):
        return f"Order item ID: {self.id}"

from sqlalchemy import (
    # String,
    Integer,
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(Integer, ForeignKey("books.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    customer_id = Column(Integer, ForeignKey("users.id"))
    paid = Column(Boolean, default=False)
    delivery_date = Column(Date, default=None)
    complete = Column(Boolean, default=False)

    customer = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"Order ID: {self.id}"

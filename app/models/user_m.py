from sqlalchemy import String, Integer, Boolean, Column
from sqlalchemy.orm import relationship


from app.database.db import Base

# from app.models.order_m import Order


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="customer")

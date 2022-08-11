from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship


from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="user")

    orders = relationship("Order", back_populates="customer")

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Column,
    Text,
    Float,
    # ForeignKey,
)

from app.database.db import Base


# class Category(Base):
#     __tablename__ = "categories"
# class Author(Base):
#     __tablename__ = "authors"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=False)

    # author_id = Column(Integer, ForeignKey("parent.id"), nullable=False)
    # category_id = Column(Integer, ForeignKey("parent.id"), nullable=False)

    def __repr__(self):
        return f"Book name: {self.name}"


# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
#
# from .database import Base
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#
#     items = relationship("Item", back_populates="owner")
#
#
# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     owner = relationship("User", back_populates="items")

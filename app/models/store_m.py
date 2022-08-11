from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Column,
    Text,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.database.db import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

    # books = relationship("Book", back_populates="category")

    def __repr__(self):
        return f"Category name: {self.name}"


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False, unique=True)
    email = Column(String(64), nullable=False)

    # books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"Author name: {self.name}"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    description = Column(Text)
    year_of_publication = Column(Integer)
    is_active = Column(Boolean)

    author_id = Column(Integer, ForeignKey("authors.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    author = relationship(
        "Author", backref="books"
    )  # , back_populates="books")
    category = relationship(
        "Category", backref="books"
    )  # , back_populates="books")

    def __repr__(self):
        return f"Book title: {self.name}"

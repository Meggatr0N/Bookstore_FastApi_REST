from sqlalchemy import String, Integer, Boolean, Column, Text, Float, ForeignKey

from .db import Base


#class Category(Base):
#    __tablename__ = "categories"
#    

#class Author(Base):
#    __tablename__ = "authors"
#    


class Book(Base):
    __tablename__='books'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=False)

    #author_id = Column(Integer, ForeignKey("parent.id"), nullable=False)
    #category_id = Column(Integer, ForeignKey("parent.id"), nullable=False)

    def __repr__(self):
        return f'Book name: {self.name}'
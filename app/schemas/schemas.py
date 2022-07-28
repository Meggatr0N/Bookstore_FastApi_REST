from pydantic import BaseModel


class Book(BaseModel):
    id: int
    name: str
    price: float
    description: str
    is_active: bool
    # author_id: int
    # category_id: int

    class Config:
        orm_mode = True


class CreatedBook(BaseModel):
    name: str
    price: float
    description: str
    is_active: bool


# from pydantic import BaseModel
#
#
# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None
#
#
# class ItemCreate(ItemBase):
#     pass
#
#
# class Item(ItemBase):
#     id: int
#     owner_id: int
#
#     class Config:
#         orm_mode = True
#
#
# class UserBase(BaseModel):
#     email: str
#
#
# class UserCreate(UserBase):
#     password: str
#
#
# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []
#
#     class Config:
#         orm_mode = True

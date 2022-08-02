from pydantic import BaseModel


class BookBase(BaseModel):
    name: str
    price: float
    description: str
    is_active: bool


class AuthorBase(BaseModel):
    name: str
    email: str


class CategoryBase(BaseModel):
    name: str


class BookCreate(BookBase):
    author_id: int = 1
    category_id: int = 1

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    is_active: bool


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class BookItem(Book):
    author: Author | None
    category: Category | None


class AuthorItem(Author):
    books: list[Book] = []


class BookForCategoryItem(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CategoryItem(Category):
    is_active: bool
    books: list[BookForCategoryItem] = []

    class Config:
        orm_mode = True

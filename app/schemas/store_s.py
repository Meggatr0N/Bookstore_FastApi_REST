from pydantic import BaseModel, Field, EmailStr


class CategoryCreate(BaseModel):
    name: str
    is_active: bool = True

    class Config:
        schema_extra = {
            "example": {
                "name": "Example category",
                "is_active": "True",
            }
        }


class CategoryChange(BaseModel):
    name: str | None
    is_active: bool | None

    class Config:
        schema_extra = {
            "example": {
                "name": "Example category",
                "is_active": "True",
            }
        }


class AuthorCreate(BaseModel):
    name: str
    email: EmailStr = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Example Author",
                "email": "exampleauthor@gmail.com",
            }
        }


class AuthorChange(BaseModel):
    name: str | None
    email: EmailStr | None

    class Config:
        schema_extra = {
            "example": {
                "name": "Example Author",
                "email": "exampleauthor@gmail.com",
            }
        }


class BookCreate(BaseModel):
    name: str
    price: float
    description: str
    year_of_publication: int
    is_active: bool = True
    author_id: int | None = None
    category_id: int | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Example Book",
                "price": "100",
                "description": "Any your description about a book",
                "year_of_publication": "2022",
                "is_active": "True",
                "author_id": "0",
                "category_id": "0",
            }
        }


class BookChange(BaseModel):
    name: str | None
    price: float | None
    description: str | None
    year_of_publication: int | None
    is_active: bool | None
    author_id: int | None
    category_id: int | None

    class Config:
        schema_extra = {
            "example": {
                "name": "Example Book",
                "price": "100",
                "description": "Any your description about a book",
                "year_of_publication": "2022",
                "is_active": "True",
                "author_id": "0",
                "category_id": "0",
            }
        }


class CategoryInListShow(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123",
                "name": "Example category",
                "is_active": "True",
            }
        }


class CategorySmallShow(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123",
                "name": "Example category",
            }
        }


class AuthorInListShow(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123",
                "name": "Example Author",
                "email": "exampleauthor@gmail.com",
            }
        }


class AuthorSmallShow(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123",
                "name": "Example Author",
            }
        }


class BookSmallShow(BaseModel):
    id: int
    name: str
    year_of_publication: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123",
                "name": "Example Book",
                "year_of_publication": "2022",
            }
        }


class CategoryFullShow(BaseModel):
    id: int
    name: str
    is_active: bool
    books: list[BookSmallShow] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123",
                "name": "Example category",
                "is_active": "True",
                "books": [
                    {
                        "id": "123",
                        "name": "Example Book",
                        "year_of_publication": "2022",
                    },
                    {
                        "id": "124",
                        "name": "Example Book2",
                        "year_of_publication": "2022",
                    },
                ],
            }
        }


class AuthorFullShow(BaseModel):
    id: int
    name: str
    email: str
    books: list[BookSmallShow] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123",
                "name": "Example Author",
                "email": "exampleauthor@gmail.com",
                "books": [
                    {
                        "id": "123",
                        "name": "Example Book",
                        "year_of_publication": "2022",
                    },
                    {
                        "id": "124",
                        "name": "Example Book2",
                        "year_of_publication": "2022",
                    },
                ],
            }
        }


class BookFullShow(BaseModel):
    id: int
    name: str
    price: float
    description: str
    year_of_publication: int
    is_active: bool
    author: AuthorSmallShow | None
    category: CategorySmallShow | None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123",
                "name": "Example Book",
                "price": "100",
                "description": "Any your description about a book",
                "year_of_publication": "2022",
                "is_active": "True",
                "author": {
                    "id": "123",
                    "name": "Example Author",
                },
                "category": {
                    "id": "123",
                    "name": "Example category",
                },
            }
        }

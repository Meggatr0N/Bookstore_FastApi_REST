from pydantic import BaseModel, Field, EmailStr

# ---------------------------------------------------------------------------------------
# CategoryCreate
# ---------------------------------------------------------------------------------------


class CategoryCreate(BaseModel):
    """
    Used to create a general info about category
    """

    name: str
    is_active: bool = True

    class Config:
        schema_extra = {
            "example": {
                "name": "Example category",
                "is_active": "True",
            }
        }


# ---------------------------------------------------------------------------------------
# CategoryChange
# ---------------------------------------------------------------------------------------


class CategoryChange(BaseModel):
    """
    Used to change a general info about category
    """

    name: str | None
    is_active: bool | None

    class Config:
        schema_extra = {
            "example": {
                "name": "Example category",
                "is_active": "True",
            }
        }


# ---------------------------------------------------------------------------------------
# AuthorCreate
# ---------------------------------------------------------------------------------------


class AuthorCreate(BaseModel):
    """
    Used to create a general info about author
    """

    name: str
    email: EmailStr = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Example Author",
                "email": "exampleauthor@gmail.com",
            }
        }


# ---------------------------------------------------------------------------------------
# AuthorChange
# ---------------------------------------------------------------------------------------


class AuthorChange(BaseModel):
    """
    Used to change a general info about author
    """

    name: str | None
    email: EmailStr | None

    class Config:
        schema_extra = {
            "example": {
                "name": "Example Author",
                "email": "exampleauthor@gmail.com",
            }
        }


# ---------------------------------------------------------------------------------------
# BookCreate
# ---------------------------------------------------------------------------------------


class BookCreate(BaseModel):
    """
    Used to create a general info about book
    """

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


# ---------------------------------------------------------------------------------------
# BookChange
# ---------------------------------------------------------------------------------------


class BookChange(BaseModel):
    """
    Used to change a general info about category
    """

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


# ---------------------------------------------------------------------------------------
# CategoryShortShow
# ---------------------------------------------------------------------------------------


class CategoryShortShow(BaseModel):
    """
    Used to show id + general info about category
    """

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


# ---------------------------------------------------------------------------------------
# AuthorInListShow
# ---------------------------------------------------------------------------------------


class AuthorInListShow(BaseModel):
    """
    Used to show id + general info about author in list of authors
    """

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


# ---------------------------------------------------------------------------------------
# AuthorShortShow
# ---------------------------------------------------------------------------------------


class AuthorShortShow(BaseModel):
    """
    Used to show info about author inside book's info
    """

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


# ---------------------------------------------------------------------------------------
# BookShortShow
# ---------------------------------------------------------------------------------------


class BookShortShow(BaseModel):
    """
    Used to show info about book inside author's or category's info
    """

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


# ---------------------------------------------------------------------------------------
# CategoryFullShow
# ---------------------------------------------------------------------------------------


class CategoryFullShow(BaseModel):
    """
    Used to show full info about category
    """

    id: int
    name: str
    is_active: bool
    books: list[BookShortShow] = []

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


# ---------------------------------------------------------------------------------------
# AuthorFullShow
# ---------------------------------------------------------------------------------------


class AuthorFullShow(BaseModel):
    """
    Used to show full info about author
    """

    id: int
    name: str
    email: str
    books: list[BookShortShow] = []

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


# ---------------------------------------------------------------------------------------
# BookFullShow
# ---------------------------------------------------------------------------------------


class BookFullShow(BaseModel):
    """
    Used to show full info about book
    """

    id: int
    name: str
    price: float
    description: str
    year_of_publication: int
    is_active: bool
    author: AuthorShortShow | None
    category: CategoryShortShow | None

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

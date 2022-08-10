from pydantic import BaseModel, Field, EmailStr, constr
from datetime import date


class UserCreate(BaseModel):
    fullname: str
    email: EmailStr = Field(...)
    password: constr(min_length=8)
    passwordConfirm: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Example User",
                "email": "exampleuser@gmail.com",
                "password": "123user123",
                "passwordConfirm": "123user123",
            }
        }


class OrderCreate(BaseModel):
    book_id: int
    quantity: int

    class Config:
        schema_extra = {
            "example": {
                "book_id": "1234",
                "quantity": "8",
            }
        }


class OrderUpdateByStaff(BaseModel):
    paid: bool | None
    delivery_date: date | None
    complete: bool | None

    class Config:
        schema_extra = {
            "example": {
                "paid": "False",
                "delivery_date": "2000-01-01",
                "complete": "False",
            }
        }


class OrderUpdateByUserHimself(BaseModel):
    book_id: int | None
    quantity: int | None

    class Config:
        schema_extra = {
            "example": {
                "book_id": "12",
                "quantity": "4",
            }
        }


class UserPermissionChange(BaseModel):
    is_staff: bool | None
    is_superuser: bool | None

    class Config:
        schema_extra = {
            "example": {
                "is_staff": "False",
                "is_superuser": "False",
            }
        }


class UserChangeByUserHimself(BaseModel):
    fullname: str | None
    email: str | None
    old_password: str | None
    new_password: constr(min_length=8) | None
    new_passwordConfirm: str | None

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Example User",
                "email": "exampleuser@gmail.com",
                "old_password": "12345678",
                "new_password": "87654321",
                "new_passwordConfirm": "87654321",
            }
        }


class UserSmallShow(BaseModel):
    id: int
    fullname: str
    email: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "7",
                "fullname": "Example User",
                "email": "exampleuser@gmail.com",
            }
        }


class UserInListOfUsersShow(BaseModel):
    id: int
    fullname: str
    email: str
    is_staff: bool
    is_superuser: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "7",
                "fullname": "Example User",
                "email": "exampleuser@gmail.com",
                "is_staff": "False",
                "is_superuser": "False",
            }
        }


class OrderSmallShow(BaseModel):
    id: int
    total_price: float
    paid: bool | None = False
    delivery_date: date | None
    complete: bool | None = False

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "12",
                "total_price": "0.00",
                "paid": "False",
                "delivery_date": "2022-01-01",
                "complete": "False",
            }
        }


class UserFullShow(BaseModel):
    id: int
    fullname: str
    email: str
    is_staff: bool
    is_superuser: bool
    orders: list[OrderSmallShow] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "7",
                "fullname": "Example User",
                "email": "exampleuser@gmail.com",
                "is_staff": "False",
                "is_superuser": "False",
                "orders": [
                    {
                        "id": "12",
                        "total_price": "450.00",
                        "paid": "True",
                        "delivery_date": "2022-01-01",
                        "complete": "False",
                    },
                    {
                        "id": "13",
                        "total_price": "1000.00",
                        "paid": "True",
                        "delivery_date": "2022-01-01",
                        "complete": "False",
                    },
                ],
            }
        }


class OrderFullShow(BaseModel):
    id: int
    book_id: int
    quantity: int
    total_price: float
    paid: bool
    customer: UserSmallShow | None
    delivery_date: date | None
    complete: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "12",
                "book_id": "12",
                "quantity": "4",
                "total_price": "0.00",
                "paid": "False",
                "customer": {
                    "id": "7",
                    "fullname": "Example User",
                    "email": "exampleuser@gmail.com",
                },
                "delivery_date": "2022-01-01",
                "complete": "False",
            }
        }

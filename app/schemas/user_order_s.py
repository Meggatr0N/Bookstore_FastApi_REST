from pydantic import BaseModel, Field, EmailStr, constr
from datetime import date


# ---------------------------------------------------------------------------------------
# UserCreate
# ---------------------------------------------------------------------------------------


class UserCreate(BaseModel):
    """
    Used to create new user
    """

    fullname: str
    email: EmailStr = Field(...)
    password: constr(min_length=8)
    passwordConfirm: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "User",
                "email": "user@gmail.com",
                "password": "qwerty12",
                "passwordConfirm": "qwerty12",
            }
        }


# ---------------------------------------------------------------------------------------
# OrderItemCreate
# ---------------------------------------------------------------------------------------


class OrderItemCreate(BaseModel):
    """
    Used inside order as item of order.
    """

    book_id: int
    quantity: int

    class Config:
        schema_extra = {
            "example": {
                "book_id": "0",
                "quantity": "1",
            }
        }


# ---------------------------------------------------------------------------------------
# OrderItemShow
# ---------------------------------------------------------------------------------------


class OrderItemShow(BaseModel):
    """
    Used to show order's items inside order.
    """

    id: int
    book_id: int
    quantity: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "41",
                "book_id": "1",
                "quantity": "5",
            },
        }


# ---------------------------------------------------------------------------------------
# OrderUpdateByStaff
# ---------------------------------------------------------------------------------------


class OrderUpdateByStaff(BaseModel):
    """
    Used to update the service information of an order.
    """

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


# ---------------------------------------------------------------------------------------
# UserPermissionChange
# ---------------------------------------------------------------------------------------


class UserPermissionChange(BaseModel):
    """
    Used to change user permissions by admin
    """

    role: str

    class Config:
        schema_extra = {
            "example": {
                "role": "user",
            }
        }


# ---------------------------------------------------------------------------------------
# UserChangeByUserHimself
# ---------------------------------------------------------------------------------------


class UserChangeByUserHimself(BaseModel):
    """
    Used to change user credentials by user himself
    """

    fullname: str | None
    email: str | None
    old_password: str | None
    new_password: constr(min_length=8) | None
    new_passwordConfirm: str | None

    class Config:
        schema_extra = {
            "example": {
                "fullname": "User",
                "email": "user@gmail.com",
                "old_password": "12345678",
                "new_password": "87654321",
                "new_passwordConfirm": "87654321",
            }
        }


# ---------------------------------------------------------------------------------------
# UserShortShow
# ---------------------------------------------------------------------------------------


class UserShortShow(BaseModel):
    """
    Used to show user main short info inside other models
    """

    id: int
    fullname: str
    email: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "7",
                "fullname": "User",
                "email": "user@gmail.com",
            }
        }


# ---------------------------------------------------------------------------------------
# UserFullShow
# ---------------------------------------------------------------------------------------


class UserFullShow(BaseModel):
    """
    Used to show full user info
    """

    id: int
    fullname: str
    email: str
    role: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "7",
                "fullname": "User",
                "email": "user@gmail.com",
                "role": "user",
            }
        }


# ---------------------------------------------------------------------------------------
# OrderShortShow
# ---------------------------------------------------------------------------------------


class OrderShortShow(BaseModel):
    """
    Used to show short main order info
    """

    id: int
    date_placed: date
    total_price: float
    paid: bool
    delivery_date: date | None
    complete: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "2",
                "date_placed": "2000/01/01",
                "total_price": "99.97",
                "paid": "False",
                "delivery_date": "2000/01/01",
                "complete": "False",
            }
        }


# ---------------------------------------------------------------------------------------
# OrderFullShow
# ---------------------------------------------------------------------------------------


class OrderFullShow(BaseModel):
    """
    Used to show full order info
    """

    id: int
    date_placed: date
    total_price: float
    customer: UserShortShow
    paid: bool
    delivery_date: date | None
    complete: bool

    line_items: list[OrderItemShow] | None = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 2,
                "date_placed": "2000/01/01",
                "total_price": "99.97",
                "customer": {
                    "id": 1,
                    "fullname": "user",
                    "email": "user@gmail.com",
                },
                "paid": "False",
                "delivery_date": "2000/01/01",
                "complete": "False",
                "order_items": [
                    {
                        "id": "41",
                        "book_id": "3",
                        "quantity": "5",
                    },
                    {
                        "id": "42",
                        "book_id": "1",
                        "quantity": "2",
                    },
                ],
            }
        }


# ---------------------------------------------------------------------------------------
# OrdersForUserShow
# ---------------------------------------------------------------------------------------


class OrdersForUserShow(BaseModel):
    """
    Used to show full order info inside list for user
    """

    id: int
    date_placed: date
    total_price: float
    paid: bool
    delivery_date: date | None
    complete: bool

    line_items: list[OrderItemShow] | None = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 2,
                "date_placed": "2000/01/01",
                "total_price": "99.97",
                "paid": "False",
                "delivery_date": "2000/01/01",
                "complete": "False",
                "order_items": [
                    {
                        "id": "41",
                        "book_id": "1",
                        "quantity": "2",
                    },
                    {
                        "id": "42",
                        "book_id": "2",
                        "quantity": "2",
                    },
                ],
            }
        }

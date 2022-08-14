import pytest
from fastapi import HTTPException

from app.crud import auth_logic
from app.models import user_m
from app.schemas import auth_s, user_order_s
from app.core import security

# ---------------------------------------------------------------------------------------
# test_get_hashed_password
# ---------------------------------------------------------------------------------------


def test_get_hashed_password():
    hashed_password = security.get_hashed_password(password="qwerty123")
    assert len(hashed_password) == 60


# ---------------------------------------------------------------------------------------
# test_verify_password
# ---------------------------------------------------------------------------------------


def test_verify_password():
    hashed_password = security.get_hashed_password(password="qwerty123")
    assert (
        security.verify_password(
            plain_password="qwerty123",
            hashed_password=hashed_password,
        )
        is True
    )


# ---------------------------------------------------------------------------------------
# test_encode_token
# ---------------------------------------------------------------------------------------


def test_encode_token():
    access_data = {
        "email": "user1@gmail.com",
        "id": "1",
        "role": "user",
    }
    refresh_data = {
        "email": "user1@gmail.com",
    }
    token1 = security.encode_token(data=access_data, type="access_token")
    token2 = security.encode_token(data=refresh_data, type="refresh_token")
    assert token1 is not None
    assert token2 is not None


# ---------------------------------------------------------------------------------------
# test_decode_access_token
# ---------------------------------------------------------------------------------------


def test_decode_access_token():
    access_data = {
        "email": "user1@gmail.com",
        "id": "1",
        "role": "user",
    }
    token = security.encode_token(data=access_data, type="access_token")
    assert token is not None
    data: auth_s.TokenData = security.decode_access_token(access_token=token)
    assert data is not None
    assert data.id == 1
    assert data.email == "user1@gmail.com"
    assert data.role == "user"


# ---------------------------------------------------------------------------------------
# test_decode_refresh_token
# ---------------------------------------------------------------------------------------


def test_decode_refresh_token():
    refresh_data = {
        "email": "user1@gmail.com",
    }
    token = security.encode_token(data=refresh_data, type="refresh_token")
    assert token is not None
    data = security.decode_refresh_token(refresh_token=token)
    assert data is not None
    assert data == "user1@gmail.com"


# ---------------------------------------------------------------------------------------
# test_check_permision
# ---------------------------------------------------------------------------------------


def test_check_permision(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }
    obj_user = user_order_s.UserCreate(**user_data)
    user1: user_m.User = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )

    with pytest.raises(HTTPException):
        security.check_permision(current_user=user1, bottom_perm="staff")

    with pytest.raises(HTTPException):
        security.check_permision(current_user=user1, bottom_perm="admin")

    with pytest.raises(HTTPException):
        security.check_permision(current_user=user1, bottom_perm="")

    user2 = user_m.User(
        fullname="User2",
        email="user2@gmail.com",
        password="12345678",
        role="staff",
    )

    user3 = user_m.User(
        fullname="User3",
        email="user3@gmail.com",
        password="12345678",
        role="admin",
    )
    db_session.add(user2)
    db_session.add(user3)
    db_session.commit()

    var2 = security.check_permision(current_user=user2, bottom_perm="staff")
    assert var2 is True
    var3 = security.check_permision(current_user=user3, bottom_perm="admin")
    assert var3 is True

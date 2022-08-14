import pytest
from fastapi import HTTPException

from app.crud import auth_logic, user_logic
from app.models import user_m
from app.schemas import user_order_s
from app.core import security

# ---------------------------------------------------------------------------------------
# test_get_all_users
# ---------------------------------------------------------------------------------------


def test_get_all_users(
    db_session,
):
    for i in range(1, 10):
        user_data = {
            "fullname": f"User{i}",
            "email": f"user{i}@gmail.com",
            "password": "12345678",
            "passwordConfirm": "12345678",
        }
        obj_user = user_order_s.UserCreate(**user_data)
        auth_logic.create_user(
            db=db_session,
            schema=obj_user,
        )

    all_users = user_logic.get_all_users(
        db=db_session,
        limit=6,
        page=2,
        reverse_sort=False,
        find_by_email=None,
        role="user",
    )
    for i, item in enumerate(all_users, start=7):
        assert item.fullname == f"User{i}"
        assert item.email == f"user{i}@gmail.com"
    assert len(all_users) == 3


# ---------------------------------------------------------------------------------------
# test_get_one_user
# ---------------------------------------------------------------------------------------


def test_get_one_user(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }
    obj_user = user_order_s.UserCreate(**user_data)
    user: user_m.User = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )
    item = user_logic.get_one_user(
        email=user.email,
        db=db_session,
    )
    assert item == user


# ---------------------------------------------------------------------------------------
# test_change_user_by_superuser
# ---------------------------------------------------------------------------------------


def test_change_user_by_superuser(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }

    obj_user = user_order_s.UserCreate(**user_data)
    user: user_m.User = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )
    user_old_role = user.role

    user_data_to_update = {"role": "staff"}
    data_to_update = user_order_s.UserPermissionChange(**user_data_to_update)

    updated_user = user_logic.change_user_by_superuser(
        email=user.email,
        schema=data_to_update,
        db=db_session,
    )
    assert updated_user.role != user_old_role
    assert updated_user.role == "staff"


# ---------------------------------------------------------------------------------------
# test_change_user_by_himself
# ---------------------------------------------------------------------------------------


def test_change_user_by_himself(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }

    obj_user = user_order_s.UserCreate(**user_data)
    user: user_m.User = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )
    user_data_to_update = {
        "fullname": "Artur 1",
        "email": "arturka@gmail.com",
        "old_password": "12345678",
        "new_password": "87654321",
        "new_passwordConfirm": "87654321",
    }
    data_to_update = user_order_s.UserChangeByUserHimself(
        **user_data_to_update
    )
    updated_user = user_logic.change_user_by_himself(
        email=user.email,
        schema=data_to_update,
        db=db_session,
    )
    assert updated_user.fullname == user_data_to_update["fullname"]
    assert updated_user.fullname != user_data["fullname"]

    assert updated_user.email == user_data_to_update["email"]
    assert updated_user.email != user_data["email"]

    old_password = security.get_hashed_password(user_data["password"])

    assert (
        security.verify_password(
            plain_password=user_data_to_update["old_password"],
            hashed_password=old_password,
        )
        is True
    )


# ---------------------------------------------------------------------------------------
# test_delete_user
# ---------------------------------------------------------------------------------------


def test_delete_user(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }

    obj_user = user_order_s.UserCreate(**user_data)
    user: user_m.User = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )

    deleted_user_info = user_logic.delete_user(
        user_id=user.id,
        db=db_session,
    )
    assert deleted_user_info == {"detail": "User deleted successfully"}

    with pytest.raises(HTTPException):
        user_logic.get_one_user(
            email=user_data["email"],
            db=db_session,
        )

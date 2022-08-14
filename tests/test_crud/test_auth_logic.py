from app.crud import auth_logic
from app.models import user_m
from app.schemas import user_order_s, auth_s


# ---------------------------------------------------------------------------------------
# test_create_user
# ---------------------------------------------------------------------------------------


def test_create_user(
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
    assert user.fullname == user_data["fullname"]
    assert user.email == user_data["email"]
    assert user.id == 1


# ---------------------------------------------------------------------------------------
# test_verify_login
# ---------------------------------------------------------------------------------------


def test_verify_login(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }
    obj_user = user_order_s.UserCreate(**user_data)
    auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )

    credentials_data = {"email": "USER1@gmail.com", "password": "12345678"}
    data_to_login = auth_s.LoginUserSchema(**credentials_data)

    login_answer = auth_logic.verify_login(
        schema=data_to_login,
        db=db_session,
    )

    should_be = ["access_token", "refresh_token", "token_type"]
    for item in should_be:
        assert item in login_answer.keys()
    login_answer["token_type"] == "bearer"

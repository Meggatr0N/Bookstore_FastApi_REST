from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.models import user_m
from app.core import security


# ---------------------------------------------------------------------------------------
# create_user
# ---------------------------------------------------------------------------------------


def create_user(
    schema: BaseModel,
    db: Session,
):
    user = (
        db.query(user_m.User)
        .filter(user_m.User.email == schema.email.lower())
        .first()
    )

    # user existence check
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exist",
        )

    # checking passwords for matching
    if schema.password != schema.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    new_user = user_m.User(
        fullname=schema.fullname,
        email=EmailStr(schema.email.lower()),
        password=security.get_hashed_password(schema.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ---------------------------------------------------------------------------------------
# verify_login
# ---------------------------------------------------------------------------------------


def verify_login(
    schema: BaseModel,
    db: Session,
):
    enter_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )

    user = (
        db.query(user_m.User)
        .filter(user_m.User.email == EmailStr(schema.email.lower()))
        .first()
    )

    # user existence check
    if not user:
        raise enter_exception

    # Check if the password is valid
    if not security.verify_password(schema.password, user.password):
        raise enter_exception

    # payload data for access token
    access_data = {
        "email": user.email,
        "id": user.id,
        "role": user.role,
    }

    # payload data for refresh token
    refresh_data = {
        "email": user.email,
    }

    # encoding tokens
    access_token = security.encode_token(access_data, "access_token")
    refresh_token = security.encode_token(refresh_data, "refresh_token")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

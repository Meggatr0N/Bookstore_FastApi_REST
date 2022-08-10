from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.models import user_m
from app.core import security

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
        .filter(user_m.User.email == EmailStr(schema.username.lower()))
        .first()
    )

    # user existence check
    if not user:
        raise enter_exception

    # Check if the password is valid
    if not security.verify_password(schema.password, user.password):
        raise enter_exception

    # payload data for jwt
    jwt_data = {
        "email": user.email,
        "id": user.id,
        "sf": user.is_staff,
        "su": user.is_superuser,
    }

    # generate JWT "access_token" tokens
    login_token = security.encode_login_token(data=jwt_data)
    return login_token

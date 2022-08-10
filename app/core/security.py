from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.schemas import token_s
from app.core import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def encode_token(data: dict, type: str):
    payload = data.copy()

    if type == "access_token":
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid type of token",
        )

    payload.update(
        {
            "exp": expire,
            "scope": type,
            "iat": datetime.now(),
        }
    )
    return jwt.encode(
        payload,
        settings.SECRET_JWT_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def encode_login_token(data: dict):
    access_token = encode_token(data, "access_token")

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


def decode_access_token(access_token: str):
    try:
        payload = jwt.decode(
            access_token,
            settings.SECRET_JWT_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload["scope"] != "access_token":
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        email: str = payload.get("email")
        id: int = payload.get("id")
        is_staff: bool = payload.get("sf")
        is_superuser: bool = payload.get("su")

        if (
            email is None
            or id is None
            or is_staff is None
            or is_superuser is None
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_data = token_s.TokenData(
            id=id,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        return token_data

    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    return decode_access_token(data)


def check_permision(current_user, bottom_perm: str = ""):
    perm_exeption = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Permission denied!",
    )

    if "is_staff" in bottom_perm:
        if current_user.is_staff or current_user.is_superuser:
            return True
        else:
            raise perm_exeption

    elif "is_superuser" in bottom_perm:
        if current_user.is_superuser:
            return True
        else:
            raise perm_exeption
    else:
        print(
            "Check_permision - Wrong logic. \
            Add bottom_perm='is_staff' or bottom_perm='is_superuser'"
        )
        return False

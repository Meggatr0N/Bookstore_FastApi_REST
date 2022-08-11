from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status, Security
from sqlalchemy.orm import Session

from app.schemas import auth_s
from app.core import settings
from app.database.dependb import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------------------------------------------------------------------------
# get_hashed_password
# ---------------------------------------------------------------------------------------


def get_hashed_password(password: str):
    return pwd_context.hash(password)


# ---------------------------------------------------------------------------------------
# verify_password
# ---------------------------------------------------------------------------------------


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------------------
# encode_token
# ---------------------------------------------------------------------------------------


def encode_token(data: dict, type: str):
    payload = data.copy()

    if type == "access_token":
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
        )
    elif type == "refresh_token":
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRES_MINUTES
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
            "iat": datetime.utcnow(),
        }
    )
    return jwt.encode(
        payload,
        settings.SECRET_JWT_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


# ---------------------------------------------------------------------------------------
# decode_access_token
# ---------------------------------------------------------------------------------------


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

        if jwt._validate_exp(payload):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        email: str = payload.get("email")
        id: int = payload.get("id")
        role: str = payload.get("role")

        if email is None or id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_data = auth_s.TokenData(
            id=id,
            email=email,
            role=role,
        )
        return token_data

    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ---------------------------------------------------------------------------------------
# decode_refresh_token
# ---------------------------------------------------------------------------------------


def decode_refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_JWT_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload["scope"] != "refresh_token":
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if jwt._validate_exp(payload):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token__from_email: str = payload.get("email")

        if token__from_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token__from_email

    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ---------------------------------------------------------------------------------------
# auth_access_wrapper
# ---------------------------------------------------------------------------------------


def auth_access_wrapper(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    token = credentials.credentials
    return decode_access_token(token)


# ---------------------------------------------------------------------------------------
# auth_refresh_wrapper
# ---------------------------------------------------------------------------------------


def auth_refresh_wrapper(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    token = credentials.credentials
    return decode_refresh_token(token)


# ---------------------------------------------------------------------------------------
# check_permision
# ---------------------------------------------------------------------------------------


def check_permision(current_user, bottom_perm: str = ""):
    perm_exeption = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Permission denied!",
    )

    if "staff" in bottom_perm:
        if current_user.role == "staff" or current_user.role == "admin":
            return True
        else:
            raise perm_exeption

    elif "admin" in bottom_perm:
        if current_user.role == "admin":
            return True
        else:
            raise perm_exeption

    else:
        raise perm_exeption

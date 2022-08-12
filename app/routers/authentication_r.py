from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import security
from app.database.dependb import get_db
from app.schemas import auth_s, user_order_s
from app.crud import auth_logic
from app.models import user_m

router = APIRouter(tags=["Authentication"])

# ---------------------------------------------------------------------------------------
# create_user
# ---------------------------------------------------------------------------------------


@router.post(
    "/signup",
    response_model=user_order_s.UserFullShow,
    status_code=status.HTTP_201_CREATED,
)
def registrate_new_user(
    schema: user_order_s.UserCreate,
    db: Session = Depends(get_db),
):
    """
    Registrate user.

        DON'T need authentication and special permissions.

    By default user will have permission:
    * role = 'user'
    """
    return auth_logic.create_user(db=db, schema=schema)


@router.post(
    "/login",
    response_model=auth_s.LoginToken,
    status_code=status.HTTP_200_OK,
)
def login(
    schema: auth_s.LoginUserSchema,
    db: Session = Depends(get_db),
):
    """
    Authentication form.

        DON'T need authentication and special permissions.


    * Email = user's email address.
    * Password = password.

    Returns access and refresh tokens.

    Using an access token requires access to some routes.
    (expire in 15 minutes)

    Using a refresh token requires to refresh access token.
    (expire in 10080 minutes = 7 days)
    """
    return auth_logic.verify_login(db=db, schema=schema)


# ---------------------------------------------------------------------------------------
# refresh_token
# ---------------------------------------------------------------------------------------


@router.get(
    "/refresh",
    response_model=auth_s.RefreshedAccessToken,
    status_code=status.HTTP_201_CREATED,
)
def refresh_access_token(
    db: Session = Depends(get_db),
    user_email: dict = Depends(security.auth_refresh_wrapper),
):
    """
    Refresh access token form.

        Need authentication with refresh token.

    Using a refresh token requires to refresh access token.
    (expire in 10080 minutes = 7 days)

    If refresh token is valid.
    *Reading user info from database
    *Creating token with new data.
    *Returns new access token (expire in 15 minutes).
    """
    user = (
        db.query(user_m.User).filter(user_m.User.email == user_email).first()
    )

    # user existence check
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    new_user_data = {
        "email": user.email,
        "id": user.id,
        "role": user.role,
    }
    # put new user data inside access_token
    new_access_token = security.encode_token(new_user_data, "access_token")
    # return new access token
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }

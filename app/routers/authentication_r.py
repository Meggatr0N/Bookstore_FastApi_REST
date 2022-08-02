from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.dependb import get_db
from fastapi.security import OAuth2PasswordRequestForm

# from app.crud import store_logic
from app.models import user_m
from app.core import security

from app.schemas import authentication_s

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    # schema: authentication_s.Login,
    schema: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(user_m.User)
        .filter(user_m.User.email == schema.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not security.verify_password(schema.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # generate JWT token
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

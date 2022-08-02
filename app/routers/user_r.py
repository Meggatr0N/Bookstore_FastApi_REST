from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import user_m
from app.schemas import user_s

# from . import models, schemas
from app.database.dependb import get_db

from app.core import security

router = APIRouter()


@router.post("/user", response_model=user_s.User)
def create_user(request: user_s.UserCreate, db: Session = Depends(get_db)):
    new_user = user_m.User(
        name=request.name,
        email=request.email,
        password=security.get_hashed_password(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user/{user_id}", response_model=user_s.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_m.User).filter(user_m.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    return user

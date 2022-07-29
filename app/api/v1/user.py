from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.schemas import schemas

# from . import models, schemas
from app.api.dependb import get_db

from app.core.security import Hash

router = APIRouter()


@router.post("/user", response_model=schemas.User)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.user.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = (
        db.query(models.user.User)
        .filter(models.user.User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    return user

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import Base
from fastapi.encoders import jsonable_encoder


def create_item(item, db: Session, item_model: Base):
    db_item = db.query(item_model).filter(item_model.name == item.name).first()
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{item_model.__name__} with name:'{item.name}' already exists",
        )

    new_item_in_data = jsonable_encoder(item)
    new_item = item_model(**new_item_in_data)

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def get_all_items(db: Session, offset: int, limit: int, item_model: Base):
    items = db.query(item_model).offset(offset).limit(limit).all()
    return items


def get_item_by_id(item_id: int, db: Session, item_model: Base):
    item = db.query(item_model).filter(item_model.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item_model.__name__} with ID {item_id} not found",
        )

    return item


def update_item_by_id(
    item_id: int, db: Session, request_item, item_model: Base
):
    item_to_update = (
        db.query(item_model).filter(item_model.id == item_id).first()
    )

    if not item_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item_model.__name__} with ID {item_id} not found",
        )

    for keyy, value in jsonable_encoder(request_item).items():
        if keyy != "id":
            db.query(item_model).filter(item_model.id == item_id).update(
                {keyy: value}
            )

    return item_to_update


def delete_item_by_id(item_id: int, db: Session, item_model: Base):
    item_to_delete = (
        db.query(item_model).filter(item_model.id == item_id).first()
    )

    if not item_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item_model.__name__} with ID {item_id} not found",
        )

    db.delete(item_to_delete)
    db.commit()

    return {
        "detail": item_model.__name__ + " deleted successfully",
        f"{item_model.__name__}": item_to_delete,
    }

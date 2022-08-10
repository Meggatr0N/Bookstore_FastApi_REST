from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from app.database.db import Base
from app.models import store_m

# ---------------------------------------------------------------------------------------
# create_item
# ---------------------------------------------------------------------------------------


def create_item(
    item: BaseModel,
    db: Session,
    item_model: Base,
):
    db_item = db.query(item_model).filter(item_model.name == item.name).first()

    # item existence check
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{item_model.__name__} with this name already exists",
        )

    # create item
    new_item_in_data = jsonable_encoder(item)
    new_item = item_model(**new_item_in_data)

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# ---------------------------------------------------------------------------------------
# get_all_items
# ---------------------------------------------------------------------------------------


def get_all_items(
    db: Session,
    latest_first: bool,
    limit: int,
    page: int,
    item_model: Base,
    active: bool = None,
    find_by_email: str = None,
):
    skip = (page - 1) * limit
    db_items = db.query(item_model)

    # sorting
    if latest_first:
        db_items = db_items.order_by(item_model.id.desc())
    else:
        db_items = db_items.order_by(item_model.id)

    # is item active?  (category)
    if active is not None:
        db_items = db_items.filter(item_model.is_active == active)

    # search by email (author)
    if find_by_email is not None:
        db_items = db_items.filter(
            item_model.email.like(f"%{find_by_email.lower()}%")
        )

    return db_items.limit(limit).offset(skip).all()


# ---------------------------------------------------------------------------------------
# get_item_by_id
# ---------------------------------------------------------------------------------------
def get_item_by_id(
    item_id: int,
    db: Session,
    item_model: Base,
):
    item = db.query(item_model).filter(item_model.id == item_id).first()

    # item existence check
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item_model.__name__} with ID {item_id} not found",
        )

    return item


# ---------------------------------------------------------------------------------------
# update_item_by_id
# ---------------------------------------------------------------------------------------


def update_item_by_id(
    item_id: int,
    db: Session,
    schema: BaseModel,
    item_model: Base,
):
    item_to_update = (
        db.query(item_model).filter(item_model.id == item_id).first()
    )
    # item existence check
    if not item_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item_model.__name__} with ID {item_id} not found",
        )

    request_data = jsonable_encoder(schema).items()
    data_to_save = dict()
    # checking if the data matches the existing data in our db_item
    # and check if the data exists at all
    # if we have new data we will update it later
    for keyy, value in request_data:
        if (
            keyy != "id"
            and value is not None
            and item_to_update.__dict__[keyy] != value
        ):
            data_to_save[keyy] = value

    if data_to_save:
        # if we have data to update
        db.query(item_model).filter(item_model.id == item_id).update(
            data_to_save
        )
        db.commit()
        db.refresh(item_to_update)
        return item_to_update
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item with such data already exists!",
        )


# ---------------------------------------------------------------------------------------
# delete_item_by_id
# ---------------------------------------------------------------------------------------


def delete_item_by_id(
    item_id: int,
    db: Session,
    item_model: Base,
):
    item_to_delete = (
        db.query(item_model).filter(item_model.id == item_id).first()
    )
    # item existence check
    if not item_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item_model.__name__} with ID {item_id} not found",
        )

    db.delete(item_to_delete)
    db.commit()

    return {"detail": item_model.__name__ + " deleted successfully"}

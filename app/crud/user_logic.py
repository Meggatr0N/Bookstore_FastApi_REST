from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.database.db import Base
from app.models import user_m
from app.core import security


# ---------------------------------------------------------------------------------------
# get_all_users
# ---------------------------------------------------------------------------------------


def get_all_users(
    db: Session,
    limit: int,
    page: int,
    reverse_sort: bool,
    find_by_email: str,
    role: str,
):
    """
    This function get all users.
    All steps described.
    """
    skip = (page - 1) * limit
    db_items = db.query(user_m.User)

    # sorting
    if reverse_sort:
        db_items = db_items.order_by(user_m.User.id.desc())
    else:
        db_items = db_items.order_by(user_m.User.id)

    # search for a match in email
    if find_by_email is not None:
        db_items = db_items.filter(
            user_m.User.email.like(f"%{find_by_email.lower()}%")
        )

    # is user is staff
    if role is not None:
        db_items = db_items.filter(user_m.User.role.like(f"%{role}%"))

    return db_items.limit(limit).offset(skip).all()


# ---------------------------------------------------------------------------------------
# get_one_user
# ---------------------------------------------------------------------------------------


def get_one_user(
    email: str,
    db: Session,
):
    """
    This function get one user by id.
    All steps described.
    """
    # user existence check
    user = db.query(user_m.User).filter(user_m.User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return user


# ---------------------------------------------------------------------------------------
# change_user_by_superuser
# ---------------------------------------------------------------------------------------


def change_user_by_superuser(
    email: str,
    schema: BaseModel,
    db: Session,
):
    """
    This function change user info.
    All steps described.
    """
    # user existence check
    user_to_update = (
        db.query(user_m.User).filter(user_m.User.email == email).first()
    )
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    request_data = jsonable_encoder(schema).items()
    data_to_save = dict()
    # checking if the data matches the existing data in our db_item
    # and check if the data exists at all
    # if we have new data we will update it later
    for keyy, value in request_data:
        if value is not None and user_to_update.__dict__[keyy] != value:
            data_to_save[keyy] = value

    # if we have valid, new data we updating
    if data_to_save:
        db.query(user_m.User).filter(user_m.User.email == email).update(
            data_to_save
        )
        db.commit()
        db.refresh(user_to_update)
        return user_to_update
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An order with such data already exists!",
        )


# ---------------------------------------------------------------------------------------
# change_user_by_himself
# ---------------------------------------------------------------------------------------


def change_user_by_himself(
    email: str,
    schema: BaseModel,
    db: Session,
):
    """
    This function change user by himself.
    All steps described.
    """
    # user existence check
    user_to_update = (
        db.query(user_m.User).filter(user_m.User.email == email).first()
    )
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    request_data = jsonable_encoder(schema).items()
    data_to_update = dict()
    # сheck if there is a value
    for keyy, value in request_data:
        if value is not None:
            data_to_update[keyy] = value

    if data_to_update:
        if "fullname" in data_to_update:
            db.query(user_m.User).filter(user_m.User.email == email).update(
                {
                    "fullname": data_to_update["fullname"],
                }
            )

        # check the entered data, it should include 3 types of passwords
        if any(
            [
                "old_password" in data_to_update,
                "new_password" in data_to_update,
                "new_passwordConfirm" in data_to_update,
            ]
        ):
            if not all(
                [
                    "old_password" in data_to_update,
                    "new_password" in data_to_update,
                    "new_passwordConfirm" in data_to_update,
                ]
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Not enought data to change password!",
                )
            else:
                # checking if the entered password matches
                # to the one in the database
                if not security.verify_password(
                    data_to_update["old_password"], user_to_update.password
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect old password",
                    )
                else:
                    # checking passwords for matching
                    if (
                        data_to_update["new_password"]
                        != data_to_update["new_passwordConfirm"]
                    ):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="New passwords do not match",
                        )
                    else:
                        # hashing new password
                        new_password_to_db = security.get_hashed_password(
                            data_to_update["new_password"]
                        )
                        db.query(user_m.User).filter(
                            user_m.User.email == email
                        ).update(
                            {
                                "password": new_password_to_db,
                            }
                        )
        # check if user with new email is exist
        if "email" in data_to_update:
            user_in_db = (
                db.query(user_m.User)
                .filter(user_m.User.email == data_to_update["email"])
                .first()
            )
            if user_in_db:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New email is already exist",
                )
            else:
                db.query(user_m.User).filter(
                    user_m.User.email == email
                ).update(
                    {
                        "email": data_to_update["email"],
                    }
                )

        db.commit()
        db.refresh(user_to_update)
        return user_to_update
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Such data already exists!",
        )


# ---------------------------------------------------------------------------------------
# delete_user
# ---------------------------------------------------------------------------------------


def delete_user(
    user_id: int,
    db: Session,
):
    """
    This function deleting user by himself or by company staff.
    All steps described.
    """

    # user existence check
    user_to_delete = (
        db.query(user_m.User).filter(user_m.User.id == user_id).first()
    )
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    db.delete(user_to_delete)
    db.commit()

    return {"detail": "User deleted successfully"}

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import date

from app.database.db import Base
from app.models import order_m, store_m
from app.core import security


def get_all_orders(
    db: Session,
    limit: int,
    page: int,
    latest_first: bool,
    total_min: float,
    total_max: float,
    owner: int,
    date_from: date,
    date_to: date,
    complete: bool,
):
    skip = (page - 1) * limit
    db_items = db.query(order_m.Order)

    # search customer orders
    if owner is not None:
        db_items = db_items.filter(order_m.Order.customer_id == owner)

    # sorting
    if latest_first:
        db_items = db_items.order_by(order_m.Order.id.desc())
    else:
        db_items = db_items.order_by(order_m.Order.id)

    # search from date to date
    if date_from and date_to:
        db_items = db_items.filter(
            order_m.Order.delivery_date.between(date_from, date_to)
        )
    elif date_from:
        db_items = db_items.filter(order_m.Order.delivery_date >= date_from)
    elif date_to:
        db_items = db_items.filter(order_m.Order.delivery_date <= date_from)

    # search from price to price
    if total_min and total_max:
        db_items = db_items.filter(
            order_m.Order.total_price.between(total_min, total_max)
        )
    elif total_min is not None:
        db_items = db_items.filter(order_m.Order.total_price >= total_min)
    elif total_max:
        db_items = db_items.filter(order_m.Order.total_price <= total_max)

    # is order completed?
    if complete is not None:
        db_items = db_items.filter(order_m.Order.complete == complete)

    return db_items.limit(limit).offset(skip).all()


def create_item(
    item,
    db: Session,
    current_user: Base,
):
    book_db = (
        db.query(store_m.Book).filter(store_m.Book.id == item.book_id).first()
    )
    # order existence check
    if not book_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {item.book_id} not found",
        )
    # create new order
    new_item = order_m.Order(
        book_id=item.book_id,
        quantity=item.quantity,
        total_price=book_db.price * item.quantity,
        paid=False,
        customer_id=current_user.id,
        delivery_date=None,
        complete=False,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def update_last_order_by_user(
    db: Session,
    schema: BaseModel,
    current_user: Base,
):
    db_item = (
        db.query(order_m.Order)
        .filter(order_m.Order.customer_id == current_user.id)
        .order_by(order_m.Order.id.desc())
        .first()
    )

    # order existence check
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Last order not found",
        )

    request_data = jsonable_encoder(schema).items()

    data_to_save = dict()
    # checking if the data matches the existing data in our db_item
    # and check if the data exists at all
    # if we have new data we will update it later
    for keyy, value in request_data:
        if value is not None and db_item.__dict__[keyy] != value:
            data_to_save[keyy] = value

    if data_to_save:
        # start. logic to update total price in our order

        if "book_id" in data_to_save:
            # if new book is exist,
            # need to recalculate total price of order the new one
            new_book = (
                db.query(store_m.Book)
                .filter(store_m.Book.id == data_to_save["book_id"])
                .first()
            )
            # new_book existence check
            if not new_book:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Book not found",
                )
            if "quantity" in data_to_save:
                new_total_price = new_book.price * data_to_save["quantity"]
            else:
                new_total_price = new_book.price * db_item.quantity

            data_to_save["total_price"] = new_total_price

        elif "quantity" in data_to_save:
            # if new book is not exist,
            # need to recalculate total price of order using the old one
            db_book = (
                db.query(store_m.Book)
                .filter(store_m.Book.id == db_item.book_id)
                .first()
            )
            new_total_price = db_book.price * data_to_save["quantity"]
            data_to_save["total_price"] = new_total_price

        db.query(order_m.Order).filter(order_m.Order.id == db_item.id).update(
            data_to_save
        )
        db.commit()
        db.refresh(db_item)
        return db_item
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An order with such data already exists!",
        )


def update_item_by_id_by_staff(
    item_id: int,
    db: Session,
    schema: BaseModel,
):
    db_item = (
        db.query(order_m.Order).filter(order_m.Order.id == item_id).first()
    )
    # order existence check
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {item_id} not found",
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
            and db_item.__dict__[keyy] != value
        ):
            data_to_save[keyy] = value

    if data_to_save:
        db.query(order_m.Order).filter(order_m.Order.id == item_id).update(
            data_to_save
        )
        db.commit()
        db.refresh(db_item)
        return db_item
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An order with such data already exists!",
        )

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import date

from app.database.db import Base
from app.models import order_m, store_m

# ---------------------------------------------------------------------------------------
# get_all_orders
# ---------------------------------------------------------------------------------------


def get_all_orders(
    db: Session,
    limit: int,
    page: int,
    latest_first: bool,
    total_min: float,
    total_max: float,
    owner: int,
    delivery_date_from: date,
    delivery_date_to: date,
    complete: bool,
    date_placed_from: date,
    date_placed_to: date,
):
    """
    This function gets from database all orders.
    All steps described.
    """
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

    # search placed date, from date to date
    if date_placed_from and date_placed_to:
        db_items = db_items.filter(
            order_m.Order.date_placed.between(date_placed_from, date_placed_to)
        )
    elif date_placed_from:
        db_items = db_items.filter(
            order_m.Order.date_placed >= date_placed_from
        )
    elif date_placed_to:
        db_items = db_items.filter(order_m.Order.date_placed <= date_placed_to)

    # search delivery date, from date to date
    if delivery_date_from and delivery_date_to:
        db_items = db_items.filter(
            order_m.Order.delivery_date.between(
                delivery_date_from, delivery_date_to
            )
        )
    elif delivery_date_from:
        db_items = db_items.filter(
            order_m.Order.delivery_date >= delivery_date_from
        )
    elif delivery_date_to:
        db_items = db_items.filter(
            order_m.Order.delivery_date <= delivery_date_to
        )

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


# ---------------------------------------------------------------------------------------
# create_item
# ---------------------------------------------------------------------------------------


def create_item(
    item,
    db: Session,
    current_user: Base,
):
    """
    This function creates new order.
    All steps described.
    """
    # creating new order which all order's items will be added
    new_order = order_m.Order(
        total_price=0.00,
        paid=False,
        customer_id=current_user.id,
        complete=False,
    )
    db.add(new_order)
    db.commit()

    # total price will change from each item
    total_price = 0

    # looping each order's item in order
    for part_of_item in item:
        book_db = (
            db.query(store_m.Book)
            .filter(store_m.Book.id == part_of_item.book_id)
            .first()
        )
        # book existence check
        if not book_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {part_of_item.book_id} not found",
            )

        # create new order
        new_order_item = order_m.OrderItem(
            order_id=new_order.id,
            book_id=part_of_item.book_id,
            quantity=part_of_item.quantity,
        )
        # adding each order's item price to Order's total price
        total_price += book_db.price * part_of_item.quantity
        db.add(new_order_item)

    # updating Order's total price
    db.query(order_m.Order).filter(order_m.Order.id == new_order.id).update(
        {"total_price": total_price}
    )

    db.commit()

    # if something goes wrong we need and we have no new order's items
    # so we need to know it
    check_for_exist_items = (
        db.query(order_m.OrderItem)
        .filter(order_m.OrderItem.order_id == new_order.id)
        .count()
    )

    # if order's items exist, we return the order
    if check_for_exist_items:
        db_item = (
            db.query(order_m.Order)
            .filter(order_m.Order.id == new_order.id)
            .first()
        )

        return db_item
    else:
        # deleting order bacause order's items is not exist
        # if something goes wrong we need to delete empty order
        delete_previous_order_items = order_m.Order.__table__.delete().where(
            order_m.Order.id == new_order.id
        )
        db.execute(delete_previous_order_items)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty entered data",
        )


# ---------------------------------------------------------------------------------------
# update_item_by_id_by_staff
# ---------------------------------------------------------------------------------------


def update_item_by_id_by_staff(
    item_id: int,
    db: Session,
    schema: BaseModel,
):
    """
    This function for update some field inside an order by staff.
    All steps described.
    """
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

    # if we got a new data to update we updating it
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


# ---------------------------------------------------------------------------------------
# get_all_user_orders
# ---------------------------------------------------------------------------------------


def get_all_user_orders(
    latest_first: bool,
    limit: int,
    page: int,
    db: Session,
    current_user: Base,
):
    """
    This function returns list of all orders of the owner (current user).
    All steps described.
    """
    skip = (page - 1) * limit
    db_items = db.query(order_m.Order).filter(
        order_m.Order.customer_id == current_user.id
    )

    # sorting
    if latest_first:
        db_items = db_items.order_by(order_m.Order.id.desc())
    else:
        db_items = db_items.order_by(order_m.Order.id)

    return db_items.limit(limit).offset(skip).all()


# ---------------------------------------------------------------------------------------
# update_order_by_id_by_user
# ---------------------------------------------------------------------------------------


def update_order_by_id_by_user(
    order_id: int,
    db: Session,
    schema: list[BaseModel],
    current_user: Base,
):
    """
    This function for updating some fields of the owner (current user).
    All steps described.
    """
    db_item = (
        db.query(order_m.Order)
        .filter(
            order_m.Order.id == order_id,
            order_m.Order.customer_id == current_user.id,
        )
        .first()
    )

    # total price will change from each item
    new_total_price = 0

    # order existence check
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    list_of_new_items_to_save = list()

    # looping each order's item in order
    for schema_item in schema:
        request_data = jsonable_encoder(schema_item).items()

        data_to_save = dict()
        entered_item_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorect data!",
        )
        # checking if the data matches the existing data in our db_item
        # and check if the data exists at all
        # if we have new data we will update it later
        for keyy, value in request_data:
            if value is not None:
                data_to_save[keyy] = value
            else:
                raise entered_item_exception

        if data_to_save:
            # start. logic to update total price in our order
            if "quantity" in data_to_save and "book_id" in data_to_save:
                book = (
                    db.query(store_m.Book)
                    .filter(store_m.Book.id == data_to_save["book_id"])
                    .first()
                )
                # new_book existence check
                if not book:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Book ID {data_to_save["book_id"]} not found',
                    )

                # adding each order's item price to Order's total price
                new_total_price += book.price * data_to_save["quantity"]

                # adding to a list of new data
                list_of_new_items_to_save.append(
                    {
                        "order_id": order_id,
                        "book_id": book.id,
                        "quantity": data_to_save["quantity"],
                    }
                )

            else:
                raise entered_item_exception
        else:
            raise entered_item_exception

    # if we got at the end the same number of items we entered in input schema
    # it depends of if we got an exception (we don't need to save this data)
    # so it will run only if all data is valid
    # also we deleting the previous order's items
    # and add new items in our order
    if len(jsonable_encoder(schema)) == len(list_of_new_items_to_save):
        # deleting the previous order's items
        delete_previous_order_items = (
            order_m.OrderItem.__table__.delete().where(
                order_m.OrderItem.order_id == order_id
            )
        )
        db.execute(delete_previous_order_items)
        db.commit()

        # adding new order items
        for list_item in list_of_new_items_to_save:
            new_order_item = order_m.OrderItem(**list_item)
            db.add(new_order_item)

        # updating "total_price" field in order
        db.query(order_m.Order).filter(
            order_m.Order.id == order_id,
            order_m.Order.customer_id == current_user.id,
        ).update({"total_price": new_total_price})

        db.commit()
        return db_item
    else:
        raise entered_item_exception


# ---------------------------------------------------------------------------------------
# delete_order_by_id
# ---------------------------------------------------------------------------------------


def delete_order_by_id(
    item_id: int,
    db: Session,
):
    """
    This function delete order by id and all related order's items.
    All steps described.
    """
    item_to_delete = (
        db.query(order_m.Order).filter(order_m.Order.id == item_id).first()
    )
    # item existence check
    if not item_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order with ID {item_id} not found",
        )

    db.delete(item_to_delete)
    db.commit()
    # delete all related order's items
    delete_previous_order_items = order_m.OrderItem.__table__.delete().where(
        order_m.OrderItem.order_id == item_id
    )

    db.execute(delete_previous_order_items)
    db.commit()

    return {"detail": "Order deleted successfully"}

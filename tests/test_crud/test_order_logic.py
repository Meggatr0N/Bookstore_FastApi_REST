import pytest
from fastapi import HTTPException

from app.crud import author_category_logic, book_logic, order_logic, auth_logic
from app.models import store_m, order_m
from app.schemas import store_s, user_order_s


def create_author_category_and_books_for_order(
    db_session,
):
    data_author = {
        "name": "Author1",
        "email": "author@gmail.com",
    }

    obj_author_in = store_s.AuthorCreate(**data_author)
    author_category_logic.create_item(
        db=db_session,
        item=obj_author_in,
        item_model=store_m.Author,
    )

    data_category = {
        "name": "Category1",
        "is_active": "True",
    }

    obj_category_in = store_s.CategoryCreate(**data_category)
    author_category_logic.create_item(
        db=db_session,
        item=obj_category_in,
        item_model=store_m.Category,
    )

    for i in range(1, 3):
        book_data = {
            "name": f"Example Book{i}",
            "price": "5.55",
            "description": f"Any your description about a book {i}",
            "year_of_publication": f"202{i}",
            "is_active": "True",
            "author_id": "1",
            "category_id": "1",
        }
        obj_in = store_s.BookCreate(**book_data)
        book_logic.create_book(
            db=db_session,
            item=obj_in,
        )


# ---------------------------------------------------------------------------------------
# test_get_all_orders
# ---------------------------------------------------------------------------------------


def test_get_all_orders(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }
    obj_user = user_order_s.UserCreate(**user_data)
    user = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )

    create_author_category_and_books_for_order(db_session=db_session)

    order_item_data = [
        {
            "book_id": "1",
            "quantity": "1",
        },
        {
            "book_id": "2",
            "quantity": "1",
        },
    ]
    for _ in range(1, 20):

        order_item = [
            user_order_s.OrderItemCreate(**item_data)
            for item_data in order_item_data
        ]

        item: order_m.Order = order_logic.create_item(
            item=order_item,
            db=db_session,
            current_user=user,
        )

    all_orders: order_m.Order = order_logic.get_all_user_orders(
        latest_first=False,
        limit=6,
        page=2,
        db=db_session,
        current_user=user,
    )
    for i, item in enumerate(all_orders, start=7):
        assert item.customer_id == user.id
        assert str(item.total_price) == "11.10"
        assert item.id == i
    assert len(all_orders) == 6


# ---------------------------------------------------------------------------------------
# test_create_item
# ---------------------------------------------------------------------------------------


def test_create_item(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }
    obj_user = user_order_s.UserCreate(**user_data)
    user = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )

    create_author_category_and_books_for_order(db_session=db_session)

    order_item_data = [
        {
            "book_id": "1",
            "quantity": "1",
        },
        {
            "book_id": "2",
            "quantity": "1",
        },
    ]

    order_item = [
        user_order_s.OrderItemCreate(**item_data)
        for item_data in order_item_data
    ]
    new_order: order_m.Order = order_logic.create_item(
        item=order_item,
        db=db_session,
        current_user=user,
    )

    assert len(new_order.order_items) == 2
    assert str(new_order.total_price) == "11.10"
    assert new_order.paid is False
    assert new_order.delivery_date is None
    assert new_order.customer_id == user.id
    assert new_order.complete is False


# ---------------------------------------------------------------------------------------
# test_update_item_by_id_by_staff
# ---------------------------------------------------------------------------------------


def test_update_item_by_id_by_staff(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }
    obj_user = user_order_s.UserCreate(**user_data)
    user = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )

    create_author_category_and_books_for_order(db_session=db_session)

    order_item_data = [
        {
            "book_id": "1",
            "quantity": "1",
        },
        {
            "book_id": "2",
            "quantity": "1",
        },
    ]

    order_item = [
        user_order_s.OrderItemCreate(**item_data)
        for item_data in order_item_data
    ]
    order: order_m.Order = order_logic.create_item(
        item=order_item,
        db=db_session,
        current_user=user,
    )

    new_order_data = {
        "paid": "True",
        "delivery_date": "2022-10-10",
    }

    new_order_info = user_order_s.OrderUpdateByStaff(**new_order_data)
    updated_order: order_m.Order = order_logic.update_item_by_id_by_staff(
        item_id=order.id,
        db=db_session,
        schema=new_order_info,
    )

    assert updated_order.paid is True
    assert str(updated_order.delivery_date) == "2022-10-10"
    assert updated_order.complete is False


# ---------------------------------------------------------------------------------------
# test_get_all_user_orders
# ---------------------------------------------------------------------------------------


def test_get_all_user_orders(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }
    obj_user = user_order_s.UserCreate(**user_data)
    user = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )

    create_author_category_and_books_for_order(db_session=db_session)

    order_item_data = [
        {
            "book_id": "1",
            "quantity": "1",
        },
        {
            "book_id": "2",
            "quantity": "1",
        },
    ]
    for _ in range(1, 20):

        order_item = [
            user_order_s.OrderItemCreate(**item_data)
            for item_data in order_item_data
        ]

        item: order_m.Order = order_logic.create_item(
            item=order_item,
            db=db_session,
            current_user=user,
        )

    all_orders: order_m.Order = order_logic.get_all_user_orders(
        latest_first=False,
        limit=6,
        page=2,
        db=db_session,
        current_user=user,
    )
    for i, item in enumerate(all_orders, start=7):
        assert item.customer_id == user.id
        assert str(item.total_price) == "11.10"
        assert item.id == i
    assert len(all_orders) == 6


# ---------------------------------------------------------------------------------------
# test_update_order_by_id_by_user
# ---------------------------------------------------------------------------------------


def test_update_order_by_id_by_user(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }
    obj_user = user_order_s.UserCreate(**user_data)
    user = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )

    create_author_category_and_books_for_order(db_session=db_session)

    order_item_data = [
        {
            "book_id": "1",
            "quantity": "1",
        },
        {
            "book_id": "2",
            "quantity": "1",
        },
    ]

    order_item = [
        user_order_s.OrderItemCreate(**item_data)
        for item_data in order_item_data
    ]
    old_order: order_m.Order = order_logic.create_item(
        item=order_item,
        db=db_session,
        current_user=user,
    )

    assert len(old_order.order_items) == 2

    new_order_item_data = [
        {
            "book_id": "1",
            "quantity": "15",
        },
    ]

    new_order_item = [
        user_order_s.OrderItemCreate(**item_data)
        for item_data in new_order_item_data
    ]
    updated_order: order_m.Order = order_logic.update_order_by_id_by_user(
        order_id=old_order.id,
        db=db_session,
        schema=new_order_item,
        current_user=user,
    )

    assert str(old_order.total_price) == "83.25"
    assert len(updated_order.order_items) == 1


# ---------------------------------------------------------------------------------------
# test_delete_order_by_id
# ---------------------------------------------------------------------------------------


def test_delete_order_by_id(
    db_session,
):
    user_data = {
        "fullname": "User1",
        "email": "user1@gmail.com",
        "password": "12345678",
        "passwordConfirm": "12345678",
    }
    obj_user = user_order_s.UserCreate(**user_data)
    user = auth_logic.create_user(
        db=db_session,
        schema=obj_user,
    )

    create_author_category_and_books_for_order(db_session=db_session)

    order_item_data = [
        {
            "book_id": "1",
            "quantity": "1",
        },
        {
            "book_id": "2",
            "quantity": "1",
        },
    ]

    order_item = [
        user_order_s.OrderItemCreate(**item_data)
        for item_data in order_item_data
    ]

    old_order: order_m.Order = order_logic.create_item(
        item=order_item,
        db=db_session,
        current_user=user,
    )
    order_to_delete_id = old_order.id
    assert len(old_order.order_items) == 2

    answer = order_logic.delete_order_by_id(
        item_id=order_to_delete_id,
        db=db_session,
    )

    assert answer == {"detail": "Order deleted successfully"}

    with pytest.raises(HTTPException):
        author_category_logic.get_item_by_id(
            item_id=order_to_delete_id,
            db=db_session,
            item_model=order_m.Order,
        )

    check_for_deleted_model_children = (
        db_session.query(order_m.OrderItem)
        .filter(order_m.OrderItem.order_id == order_to_delete_id)
        .all()
    )
    assert len(check_for_deleted_model_children) == 0

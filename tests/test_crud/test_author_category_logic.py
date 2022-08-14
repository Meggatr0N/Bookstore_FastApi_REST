import pytest
from fastapi import HTTPException

from app.crud import author_category_logic, book_logic
from app.models import store_m
from app.schemas import store_s

# ---------------------------------------------------------------------------------------
# test_create
# ---------------------------------------------------------------------------------------


def test_create_author_item(
    db_session,
):
    data_author = {
        "name": "Author1",
        "email": "author@gmail.com",
    }

    obj_author_in = store_s.AuthorCreate(**data_author)
    item: store_m.Author = author_category_logic.create_item(
        db=db_session,
        item=obj_author_in,
        item_model=store_m.Author,
    )
    assert item.name == data_author["name"]
    assert item.email == data_author["email"]


def test_create_author_with_the_same_name(
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

    obj_author_in2 = store_s.AuthorCreate(**data_author)

    with pytest.raises(HTTPException):
        author_category_logic.create_item(
            db=db_session,
            item=obj_author_in2,
            item_model=store_m.Author,
        )


def test_create_category_with_the_same_name(
    db_session,
):
    data_category = {
        "name": "Category 1",
        "is_active": "True",
    }
    obj_category_in = store_s.CategoryCreate(**data_category)
    author_category_logic.create_item(
        db=db_session,
        item=obj_category_in,
        item_model=store_m.Category,
    )

    obj_category_in2 = store_s.CategoryCreate(**data_category)

    with pytest.raises(HTTPException):
        author_category_logic.create_item(
            db=db_session,
            item=obj_category_in2,
            item_model=store_m.Category,
        )


# ---------------------------------------------------------------------------------------
# test_get_all_items
# ---------------------------------------------------------------------------------------
def test_get_all_items_author(
    db_session,
):
    for i in range(1, 20):
        book_data = {
            "name": f"Author{i}",
            "email": f"author{i}@gmail.com",
        }
        obj_in = store_s.AuthorCreate(**book_data)
        author_category_logic.create_item(
            db=db_session,
            item=obj_in,
            item_model=store_m.Author,
        )

    item_list = author_category_logic.get_all_items(
        db=db_session,
        latest_first=False,
        limit=6,
        page=2,
        item_model=store_m.Author,
    )
    for i, item in enumerate(item_list, start=7):
        assert item.name == f"Author{i}"
    assert len(item_list) == 6


def test_get_all_items_category(
    db_session,
):
    for i in range(1, 20):
        data_category = {
            "name": f"Category{i}",
            "is_active": "True",
        }
        obj_category_in = store_s.CategoryCreate(**data_category)
        author_category_logic.create_item(
            db=db_session,
            item=obj_category_in,
            item_model=store_m.Category,
        )

    item_list = author_category_logic.get_all_items(
        db=db_session,
        latest_first=False,
        limit=6,
        page=2,
        item_model=store_m.Category,
    )
    for i, item in enumerate(item_list, start=7):
        assert item.name == f"Category{i}"
    assert len(item_list) == 6


# ---------------------------------------------------------------------------------------
# test_get_item_by_id
# ---------------------------------------------------------------------------------------


def test_get_item_by_id_author(
    db_session,
):
    data_author = {
        "name": "Author1",
        "email": "author@gmail.com",
    }

    obj_author_in = store_s.AuthorCreate(**data_author)
    item: store_m.Author = author_category_logic.create_item(
        db=db_session,
        item=obj_author_in,
        item_model=store_m.Author,
    )

    item2: store_m.Author = author_category_logic.get_item_by_id(
        item_id=item.id,
        db=db_session,
        item_model=store_m.Author,
    )
    assert item == item2


def test_get_item_by_id_category(
    db_session,
):
    data_category = {
        "name": "Category 1",
        "is_active": "True",
    }
    obj_category_in = store_s.CategoryCreate(**data_category)
    item: store_m.Category = author_category_logic.create_item(
        db=db_session,
        item=obj_category_in,
        item_model=store_m.Category,
    )

    item2: store_m.Category = author_category_logic.get_item_by_id(
        item_id=item.id,
        db=db_session,
        item_model=store_m.Category,
    )
    assert item == item2


# ---------------------------------------------------------------------------------------
# test_update_item_by_id
# ---------------------------------------------------------------------------------------


def test_update_item_by_id_author(
    db_session,
):
    old_data_author = {
        "name": "Author1",
        "email": "author@gmail.com",
    }

    obj_setup = store_s.AuthorCreate(**old_data_author)
    old_author: store_m.Author = author_category_logic.create_item(
        db=db_session,
        item=obj_setup,
        item_model=store_m.Author,
    )

    new_data_author = {
        "name": "The best author in the world",
    }
    obj_in = store_s.AuthorChange(**new_data_author)
    updated_item: store_m.Author = author_category_logic.update_item_by_id(
        item_id=old_author.id,
        db=db_session,
        schema=obj_in,
        item_model=store_m.Author,
    )
    assert updated_item.name != old_data_author["name"]
    assert updated_item.name == new_data_author["name"]


def test_update_item_by_id_category(
    db_session,
):
    old_data_category = {
        "name": "Category 1",
        "is_active": "True",
    }

    obj_setup = store_s.CategoryCreate(**old_data_category)
    old_category: store_m.Category = author_category_logic.create_item(
        db=db_session,
        item=obj_setup,
        item_model=store_m.Category,
    )

    new_data_category = {"is_active": "False"}
    obj_in = store_s.CategoryChange(**new_data_category)
    updated_item: store_m.Category = author_category_logic.update_item_by_id(
        item_id=old_category.id,
        db=db_session,
        schema=obj_in,
        item_model=store_m.Category,
    )
    assert updated_item.is_active != old_data_category["is_active"]
    assert str(updated_item.is_active) == new_data_category["is_active"]


# ---------------------------------------------------------------------------------------
# test_delete_item_by_id
# ---------------------------------------------------------------------------------------


def test_delete_item_by_id(db_session):
    old_data_author = {
        "name": "Author1",
        "email": "author@gmail.com",
    }

    obj_setup = store_s.AuthorCreate(**old_data_author)
    author_to_delete: store_m.Author = author_category_logic.create_item(
        db=db_session,
        item=obj_setup,
        item_model=store_m.Author,
    )

    item_in_database = author_category_logic.get_item_by_id(
        item_id=author_to_delete.id,
        db=db_session,
        item_model=store_m.Author,
    )
    assert author_to_delete == item_in_database

    author_category_logic.delete_item_by_id(
        item_id=author_to_delete.id,
        db=db_session,
        item_model=store_m.Author,
    )

    with pytest.raises(HTTPException):
        author_category_logic.get_item_by_id(
            item_id=author_to_delete.id,
            db=db_session,
            item_model=store_m.Author,
        )


# ---------------------------------------------------------------------------------------
# test_show_all_books_of_related_model
# ---------------------------------------------------------------------------------------


def test_show_all_books_of_related_model(
    db_session,
):
    data_author = {
        "name": "Author1",
        "email": "author@gmail.com",
    }

    obj_author_in = store_s.AuthorCreate(**data_author)
    author = author_category_logic.create_item(
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

    for i in range(1, 20):
        book_data = {
            "name": f"Example Book{i}",
            "price": "100",
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

    item_list = author_category_logic.show_all_books_of_related_model(
        item_id=author.id,
        db=db_session,
        latest_first=False,
        limit=6,
        page=2,
        related_model="author",
    )
    for i, item in enumerate(item_list, start=7):
        assert item.name == f"Example Book{i}"
        assert item.author_id == author.id
    assert len(item_list) == 6

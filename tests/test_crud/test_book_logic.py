import pytest
from fastapi import HTTPException

from app.crud import book_logic, author_category_logic
from app.models import store_m
from app.schemas import store_s


books_data = [
    (
        {
            "name": "Book1",
            "price": "3.97",
            "description": "Any your description about a book",
            "year_of_publication": "2022",
            "is_active": "True",
            "author_id": "1",
            "category_id": "1",
        }
    ),
    (
        {
            "name": "2 book",
            "price": "5.68",
            "description": "",
            "year_of_publication": "2049",
            "is_active": "False",
            "author_id": "1",
            "category_id": "1",
        }
    ),
]


def create_author_and_category_for_book(
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


@pytest.mark.parametrize("book_data", books_data)
def test_create_book(
    db_session,
    book_data,
):
    create_author_and_category_for_book(db_session=db_session)

    obj_in = store_s.BookCreate(**book_data)
    item: store_m.Book = book_logic.create_book(
        db=db_session,
        item=obj_in,
    )
    assert item.name == book_data["name"]


def test_get_all_book(
    db_session,
):
    create_author_and_category_for_book(db_session=db_session)

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

    item_list = book_logic.get_all_book(
        db=db_session,
        page=2,
        limit=6,
        reverse_sort=False,
        book_active=True,
        search_by_autor_id=None,
        search_by_category_id=None,
        categories_active=None,
    )
    for i, item in enumerate(item_list, start=7):
        assert item.name == f"Example Book{i}"
    assert len(item_list) == 6


def test_update_book(
    db_session,
):
    create_author_and_category_for_book(db_session=db_session)

    old_book_data = {
        "name": "Test3",
        "price": "100",
        "description": "Any your description about a book ",
        "year_of_publication": "2024",
        "is_active": "False",
        "author_id": "1",
        "category_id": "1",
    }
    obj_setup = store_s.BookCreate(**old_book_data)
    old_book: store_m.Book = book_logic.create_book(
        db=db_session,
        item=obj_setup,
    )

    new_data = {
        "name": "I want to change the world!",
        "price": "35.35",
        "description": "ha ha ha",
        "year_of_publication": 1991,
        "is_active": False,
    }
    obj_in = store_s.BookChange(**new_data)
    updated_book: store_m.Book = book_logic.update_book(
        db=db_session,
        item_id=old_book.id,
        schema=obj_in,
    )
    assert updated_book.name != old_book_data["name"]
    assert updated_book.name == new_data["name"]
    assert str(updated_book.price) == new_data["price"]
    assert updated_book.description == new_data["description"]
    assert updated_book.year_of_publication == new_data["year_of_publication"]
    assert updated_book.is_active == new_data["is_active"]


def test_create_book_with_wrong_author(
    db_session,
):
    create_author_and_category_for_book(db_session=db_session)
    book_data = {
        "name": "Book1",
        "price": "3.97",
        "description": "Any your description about a book",
        "year_of_publication": "2022",
        "is_active": "True",
        "author_id": "666",
        "category_id": "1",
    }

    obj_in = store_s.BookCreate(**book_data)

    with pytest.raises(HTTPException):
        book_logic.create_book(
            db=db_session,
            item=obj_in,
        )


def test_create_book_with_wrong_category(
    db_session,
):
    create_author_and_category_for_book(db_session=db_session)
    book_data = {
        "name": "Book1",
        "price": "3.97",
        "description": "Any your description about a book",
        "year_of_publication": "2022",
        "is_active": "True",
        "author_id": "1",
        "category_id": "666",
    }

    obj_in = store_s.BookCreate(**book_data)

    with pytest.raises(HTTPException):
        book_logic.create_book(
            db=db_session,
            item=obj_in,
        )

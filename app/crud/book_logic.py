from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from app.models import store_m

# ---------------------------------------------------------------------------------------
# create_book
# ---------------------------------------------------------------------------------------


def create_book(
    item: BaseModel,
    db: Session,
):
    db_item = (
        db.query(store_m.Book).filter(store_m.Book.name == item.name).first()
    )
    # item existence check
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{store_m.Book.__name__} with this name already exists",
        )

    request_data = jsonable_encoder(item)

    # check if the data exists at all
    if "author_id" in request_data:
        author_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author not found!",
        )
        bookauthor = (
            db.query(store_m.Author)
            .filter(store_m.Author.id == request_data["author_id"])
            .first()
        )
        if not bookauthor:
            raise author_exception

    if "category_id" in request_data:
        category_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found!",
        )

        bookcategory = (
            db.query(store_m.Category)
            .filter(store_m.Category.id == request_data["category_id"])
            .first()
        )

        if not bookcategory:
            raise category_exception

    new_item = store_m.Book(**request_data)

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# ---------------------------------------------------------------------------------------
# get_all_book
# ---------------------------------------------------------------------------------------


def get_all_book(
    db: Session,
    limit: int,
    page: int,
    reverse_sort: bool,
    book_active: bool,
    search_by_autor_id: int,
    search_by_category_id: int,
    categories_active: bool,
):
    skip = (page - 1) * limit

    db_items = db.query(store_m.Book)

    # shows book only with active Category (Category.is_active == True)
    if categories_active is not None:
        db_items = db_items.join(store_m.Category).filter(
            store_m.Category.is_active.is_(categories_active)
        )

    # sorting
    if reverse_sort:
        db_items = db_items.order_by(store_m.Book.id.desc())
    else:
        db_items = db_items.order_by(store_m.Book.id)

    # search for matching author
    if search_by_autor_id is not None:
        db_items = db_items.filter(
            store_m.Book.author_id == search_by_autor_id
        )

    # search for matching category
    if search_by_category_id is not None:
        db_items = db_items.filter(
            store_m.Book.category_id == search_by_category_id
        )

    # is Book active
    if book_active is not None:
        db_items = db_items.filter(store_m.Book.is_active == book_active)

    return db_items.limit(limit).offset(skip).all()


# ---------------------------------------------------------------------------------------
# update_book
# ---------------------------------------------------------------------------------------


def update_book(
    item_id: int,
    db: Session,
    schema: BaseModel,
):
    book_to_update = (
        db.query(store_m.Book).filter(store_m.Book.id == item_id).first()
    )

    # item existence check
    if not book_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{store_m.Book.__name__} with ID {item_id} not found",
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
            and book_to_update.__dict__[keyy] != value
        ):
            data_to_save[keyy] = value

    # check if the author_id exists in database
    if "author_id" in data_to_save:
        bookauthor = (
            db.query(store_m.Author)
            .filter(store_m.Author.id == data_to_save["author_id"])
            .first()
        )
        if not bookauthor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Author not found!",
            )
    # check if the category_id exists in database
    if "category_id" in data_to_save:
        bookcategory = (
            db.query(store_m.Category)
            .filter(store_m.Category.id == data_to_save["category_id"])
            .first()
        )

        if not bookcategory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found!",
            )

    if data_to_save:
        db.query(store_m.Book).filter(store_m.Book.id == item_id).update(
            data_to_save
        )
        db.commit()
        db.refresh(book_to_update)
        return book_to_update
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An order with such data already exists!",
        )

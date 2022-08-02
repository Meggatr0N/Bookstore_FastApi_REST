from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models import store_m
from app.schemas import store_s, user_s

from app.database.dependb import get_db
from app.crud import store_logic
from app.core.security import get_current_user

router = APIRouter()

# ---------------------------------------------------------------------------------------
# Book routers
# ---------------------------------------------------------------------------------------


@router.get(
    "/books",
    response_model=list[store_s.BookItem],
    status_code=status.HTTP_200_OK,
    tags=["Book"],
)
def get_all_books(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
):
    return store_logic.get_all_items(
        db=db, offset=offset, limit=limit, item_model=store_m.Book
    )


@router.get(
    "/books/{book_id}",
    response_model=store_s.BookItem,
    status_code=status.HTTP_200_OK,
    tags=["Book"],
)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    return store_logic.get_item_by_id(
        item_id=book_id, db=db, item_model=store_m.Book
    )


@router.post(
    "/books",
    response_model=store_s.BookItem,
    status_code=status.HTTP_201_CREATED,
    tags=["Book"],
)
def create_book(
    book: store_s.BookCreate,
    db: Session = Depends(get_db),
    current_user: user_s.User = Depends(get_current_user),
):
    return store_logic.create_item(item=book, db=db, item_model=store_m.Book)


@router.put(
    "/books/{book_id}",
    response_model=store_s.BookItem,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Book"],
)
def update_book_by_id(
    book_id: int,
    book: store_s.BookCreate,
    db: Session = Depends(get_db),
    current_user: user_s.User = Depends(get_current_user),
):
    return store_logic.update_item_by_id(
        item_id=book_id, db=db, schema=book, item_model=store_m.Book
    )


# mb use status code 204, but it doesn't return deleted object
@router.delete(
    "/books/{book_id}", status_code=status.HTTP_200_OK, tags=["Book"]
)
def delete_book_by_id(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: user_s.User = Depends(get_current_user),
):
    return store_logic.delete_item_by_id(
        item_id=book_id, db=db, item_model=store_m.Book
    )


# ---------------------------------------------------------------------------------------
# Categories routers
# ---------------------------------------------------------------------------------------


@router.get(
    "/categories",
    response_model=list[store_s.CategoryItem],
    status_code=status.HTTP_200_OK,
    tags=["Category"],
)
def get_all_categories(
    db: Session = Depends(get_db), offset: int = 0, limit: int = 100
):
    return store_logic.get_all_items(
        db=db, offset=offset, limit=limit, item_model=store_m.Category
    )


@router.get(
    "/categories/{category_id}",
    response_model=store_s.CategoryItem,
    status_code=status.HTTP_200_OK,
    tags=["Category"],
)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return store_logic.get_item_by_id(
        item_id=category_id, db=db, item_model=store_m.Category
    )


@router.post(
    "/categories",
    response_model=store_s.CategoryItem,
    status_code=status.HTTP_201_CREATED,
    tags=["Category"],
)
def create_category(
    category: store_s.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: user_s.User = Depends(get_current_user),
):
    return store_logic.create_item(
        item=category, db=db, item_model=store_m.Category
    )


@router.put(
    "/categories/{category_id}",
    response_model=store_s.CategoryItem,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Category"],
)
def update_category_by_id(
    category_id: int,
    category: store_s.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: user_s.User = Depends(get_current_user),
):
    return store_logic.update_item_by_id(
        item_id=category_id,
        db=db,
        schema=category,
        item_model=store_m.Category,
    )


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    tags=["Category"],
)
def delete_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: user_s.User = Depends(get_current_user),
):
    return store_logic.delete_item_by_id(
        item_id=category_id, db=db, item_model=store_m.Category
    )


# ---------------------------------------------------------------------------------------
# Author routers
# ---------------------------------------------------------------------------------------

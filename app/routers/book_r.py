from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.models import store_m
from app.schemas import store_s
from app.database.dependb import get_db
from app.crud import author_category_logic, book_logic
from app.core import security

router = APIRouter()


# ---------------------------------------------------------------------------------------
# get_all_books
# ---------------------------------------------------------------------------------------


@router.get(
    "/books",
    response_model=list[store_s.BookFullShow],
    status_code=status.HTTP_200_OK,
    tags=["Book"],
)
def get_all_books(
    db: Session = Depends(get_db),
    latest_first: bool = Query(
        True, description="Get the latest added books (from end to start)"
    ),
    limit: int = 10,
    page: int = 1,
    active_books: bool = Query(True, description="books active or inactive"),
    active_categories: bool = Query(
        True,
        description="books whose category active or inactive",
    ),
    autor: int | None = Query(None, description="Search books by author id"),
    category: int
    | None = Query(None, description="Search books by category id"),
):
    """
    Get all books.

        DON'T need authentication and special permissions.


    You can use query parameters to get some specific information as:

    * latest_first...   True shows list from end to start.
    * book_active... shows active or inattive books
    * categories_active... shows books whose category is active or inactive
    * autor... shows books with an author who has this id
    * category... shows books with category who have this id
    """
    return book_logic.get_all_book(
        db=db,
        page=page,
        limit=limit,
        reverse_sort=latest_first,
        book_active=active_books,
        search_by_autor_id=autor,
        search_by_category_id=category,
        categories_active=active_categories,
    )


# ---------------------------------------------------------------------------------------
# create_book
# ---------------------------------------------------------------------------------------


@router.post(
    "/books",
    response_model=store_s.BookFullShow,
    status_code=status.HTTP_201_CREATED,
    tags=["Book"],
)
def create_book(
    book: store_s.BookCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Create book.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return book_logic.create_book(
            item=book,
            db=db,
        )


# ---------------------------------------------------------------------------------------
# get_book_by_id
# ---------------------------------------------------------------------------------------


@router.get(
    "/books/{book_id}",
    response_model=store_s.BookFullShow,
    status_code=status.HTTP_200_OK,
    tags=["Book"],
)
def get_book_by_id(
    book_id: int,
    db: Session = Depends(get_db),
):
    """
    Get full information about one book by ID.

        DON'T need authentication and special permissions.
    """
    return author_category_logic.get_item_by_id(
        item_id=book_id,
        db=db,
        item_model=store_m.Book,
    )


# ---------------------------------------------------------------------------------------
# update_book_by_id
# ---------------------------------------------------------------------------------------


@router.put(
    "/books/{book_id}",
    response_model=store_s.BookFullShow,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Book"],
)
def update_book_by_id(
    book_id: int,
    book: store_s.BookChange,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Update book by ID.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return book_logic.update_book(
            item_id=book_id,
            db=db,
            schema=book,
        )


# ---------------------------------------------------------------------------------------
# delete_book_by_id
# ---------------------------------------------------------------------------------------

# mb use status code 204, but it doesn't return deleted object
@router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    tags=["Book"],
)
def delete_book_by_id(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Delete book by ID.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return author_category_logic.delete_item_by_id(
            item_id=book_id,
            db=db,
            item_model=store_m.Book,
        )

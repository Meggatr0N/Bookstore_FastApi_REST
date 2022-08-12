from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.models import store_m
from app.schemas import store_s
from app.database.dependb import get_db
from app.crud import author_category_logic
from app.core import security

router = APIRouter(tags=["Book authors"])

# ---------------------------------------------------------------------------------------
# get_all_authors
# ---------------------------------------------------------------------------------------


@router.get(
    "/authors",
    response_model=list[store_s.AuthorInListShow],
    status_code=status.HTTP_200_OK,
)
def get_all_authors(
    db: Session = Depends(get_db),
    latest_first: bool = Query(
        True, description="Get the latest added books (from end to start)"
    ),
    limit: int = 20,
    page: int = 1,
    find_by_email: str | None = None,
):
    """
    Get all authors.

        DON'T need authentication and special permissions.


    You can use query parameters to get some specific information as:

    * latest_first...   True shows list from end to start.
    * find_by_email... searching matching this author's email
    """
    return author_category_logic.get_all_items(
        db=db,
        page=page,
        limit=limit,
        item_model=store_m.Author,
        latest_first=latest_first,
        find_by_email=find_by_email,
    )


# ---------------------------------------------------------------------------------------
# create_author
# ---------------------------------------------------------------------------------------


@router.post(
    "/authors",
    response_model=store_s.AuthorFullShow,
    status_code=status.HTTP_201_CREATED,
)
def create_author(
    author: store_s.AuthorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Create author.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return author_category_logic.create_item(
            item=author,
            db=db,
            item_model=store_m.Author,
        )


# ---------------------------------------------------------------------------------------
# get_author_by_id
# ---------------------------------------------------------------------------------------


@router.get(
    "/authors/{authors_id}",
    response_model=store_s.AuthorFullShow,
    status_code=status.HTTP_200_OK,
)
def get_author_by_id(
    category_id: int,
    db: Session = Depends(get_db),
):
    """
    Get full information about one author by ID.

        DON'T need authentication and special permissions.
    """
    return author_category_logic.get_item_by_id(
        item_id=category_id,
        db=db,
        item_model=store_m.Author,
    )


# ---------------------------------------------------------------------------------------
# update_author_by_id
# ---------------------------------------------------------------------------------------


@router.put(
    "/authors/{authors_id}",
    response_model=store_s.AuthorFullShow,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_author_by_id(
    author_id: int,
    author: store_s.AuthorChange,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Change author by id.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return author_category_logic.update_item_by_id(
            item_id=author_id,
            db=db,
            schema=author,
            item_model=store_m.Author,
        )


# ---------------------------------------------------------------------------------------
# delete_author_by_id
# ---------------------------------------------------------------------------------------


@router.delete(
    "/authors/{authors_id}",
    status_code=status.HTTP_200_OK,
)
def delete_author_by_id(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Delete author by id.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return author_category_logic.delete_item_by_id(
            item_id=author_id,
            db=db,
            item_model=store_m.Author,
        )


# ---------------------------------------------------------------------------------------
# show_all_books_of_author
# ---------------------------------------------------------------------------------------


@router.get(
    "/author-books/{author_id}",
    response_model=list[store_s.BookShortShow],
    status_code=status.HTTP_200_OK,
)
def show_all_books_of_author_by_id(
    author_id: int,
    db: Session = Depends(get_db),
    latest_first: bool = Query(
        True, description="Get the latest added books (from end to start)"
    ),
    limit: int = 10,
    page: int = 1,
    active: bool | None = None,
):
    """
    Get all author's books short info by author id.

        DON'T need authentication and special permissions.

    You can use query parameters to get some specific information as:

    * latest_first...   True shows list from end to start.
    """
    return author_category_logic.show_all_books_of_related_model(
        item_id=author_id,
        db=db,
        page=page,
        limit=limit,
        related_model="author",
        latest_first=latest_first,
    )

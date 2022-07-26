from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.models import store_m
from app.schemas import store_s
from app.database.dependb import get_db
from app.crud import author_category_logic
from app.core import security

router = APIRouter(tags=["Category"])


# ---------------------------------------------------------------------------------------
# get_all_categories
# ---------------------------------------------------------------------------------------


@router.get(
    "/categories",
    response_model=list[store_s.CategoryShortShow],
    status_code=status.HTTP_200_OK,
)
def get_all_categories(
    db: Session = Depends(get_db),
    latest_first: bool = Query(
        True, description="Get the latest added books (from end to start)"
    ),
    limit: int = 10,
    page: int = 1,
    active: bool | None = None,
):
    """
    Get all categories.

        DON'T need authentication and special permissions.


    You can use query parameters to get some specific information as:

    * latest_first...   True shows list from end to start.
    * active... shows active categories or not
    """
    return author_category_logic.get_all_items(
        db=db,
        page=page,
        limit=limit,
        item_model=store_m.Category,
        latest_first=latest_first,
        active=active,
    )


# ---------------------------------------------------------------------------------------
# create_category
# ---------------------------------------------------------------------------------------


@router.post(
    "/categories",
    response_model=store_s.CategoryFullShow,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: store_s.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Create category.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return author_category_logic.create_item(
            item=category,
            db=db,
            item_model=store_m.Category,
        )


# ---------------------------------------------------------------------------------------
# get_category_by_id
# ---------------------------------------------------------------------------------------


@router.get(
    "/categories/{category_id}",
    response_model=store_s.CategoryFullShow,
    status_code=status.HTTP_200_OK,
)
def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
):
    """
    Get full information about one category by ID.

        DON'T need authentication and special permissions.
    """
    return author_category_logic.get_item_by_id(
        item_id=category_id,
        db=db,
        item_model=store_m.Category,
    )


# ---------------------------------------------------------------------------------------
# update_category_by_id
# ---------------------------------------------------------------------------------------


@router.put(
    "/categories/{category_id}",
    response_model=store_s.CategoryFullShow,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_category_by_id(
    category_id: int,
    category: store_s.CategoryChange,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Change category by id.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return author_category_logic.update_item_by_id(
            item_id=category_id,
            db=db,
            schema=category,
            item_model=store_m.Category,
        )


# ---------------------------------------------------------------------------------------
# delete_category_by_id
# ---------------------------------------------------------------------------------------


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_200_OK,
)
def delete_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Delete category by id.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return author_category_logic.delete_item_by_id(
            item_id=category_id,
            db=db,
            item_model=store_m.Category,
        )


# ---------------------------------------------------------------------------------------
# show_all_books_of_category_by_id
# ---------------------------------------------------------------------------------------


@router.get(
    "/category-books/{category_id}",
    response_model=list[store_s.BookFullShow],
    status_code=status.HTTP_200_OK,
)
def show_all_books_of_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
    latest_first: bool = Query(
        True, description="Get the latest added books (from end to start)"
    ),
    limit: int = 10,
    page: int = 1,
    active: bool | None = None,
):
    """
    Get all category's books short info by category id.

        DON'T need authentication and special permissions.

    You can use query parameters to get some specific information as:

    * latest_first...   True shows list from end to start.
    """
    return author_category_logic.show_all_books_of_related_model(
        item_id=category_id,
        db=db,
        page=page,
        limit=limit,
        related_model="category",
        latest_first=latest_first,
    )

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas import user_order_s
from app.database.dependb import get_db
from app.core import security
from app.crud import user_logic

router = APIRouter(tags=["Users"])


# ---------------------------------------------------------------------------------------
# get_all_users
# ---------------------------------------------------------------------------------------


@router.get(
    "/users",
    response_model=list[user_order_s.UserShortShow],
    status_code=status.HTTP_200_OK,
)
def get_all_users(
    latest_first: bool = True,
    limit: int = 10,
    page: int = 1,
    email: str | None = None,
    role: str | None = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Get all users.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.

    You can use query parameters to get some specific information as:
    * latest_first...   True shows list from end to start.
    * email... 'rt' shows every email that contains it
    * role... shows Users role
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return user_logic.get_all_users(
            db=db,
            limit=limit,
            page=page,
            reverse_sort=latest_first,
            find_by_email=email,
            role=role,
        )


# ---------------------------------------------------------------------------------------
# get_user_by_email
# ---------------------------------------------------------------------------------------


@router.get(
    "/users/{email}",
    response_model=user_order_s.UserFullShow,
    status_code=status.HTTP_200_OK,
)
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Get full information about user by email

        Need authentication and special permissions!

        Only a user who has role='staff' or role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="is_staff"):
        return user_logic.get_one_user(
            email=email,
            db=db,
        )


# ---------------------------------------------------------------------------------------
# change_user_permission_by_email_by_superuser
# ---------------------------------------------------------------------------------------


@router.put(
    "/users/{email}",
    response_model=user_order_s.UserFullShow,
    status_code=status.HTTP_202_ACCEPTED,
)
def change_user_permission_by_email_by_superuser(
    email: str,
    schema: user_order_s.UserPermissionChange,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Change user permission by email

        Need authentication and special permissions!

        Only a user who has role='admin' can get access.
    """
    if security.check_permision(current_user, bottom_perm="admin"):
        return user_logic.change_user_by_superuser(
            email=email,
            schema=schema,
            db=db,
        )


# ---------------------------------------------------------------------------------------
# delete_user_by_id
# ---------------------------------------------------------------------------------------


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
)
def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Delete user by email.

        Need authentication and/or special permissions!

        If it's your own email you can delete your account.

        Also a users who has role='staff' or role='admin' can delete as well.
    """
    # permision check inside user_logic.delete_user()
    return user_logic.delete_user(
        user_id=user_id,
        db=db,
        current_user=current_user,
    )


# ---------------------------------------------------------------------------------------
# read_current_user_info
# ---------------------------------------------------------------------------------------


@router.get(
    "/me/",
    response_model=user_order_s.UserFullShow,
    status_code=status.HTTP_200_OK,
)
def read_current_user_info(
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Get full information about current user.

        Need authentication and don't need special permissions!

        Only owner can see this info.

    But users who has special permissions as role='staff' or role='admin'
    also can see your info but using "/users/{email}"
    """
    return user_logic.get_one_user(
        email=current_user.email,
        db=db,
    )


# ---------------------------------------------------------------------------------------
# change_user_info_by_himself
# ---------------------------------------------------------------------------------------


@router.put(
    "/me/",
    response_model=user_order_s.UserFullShow,
    status_code=status.HTTP_202_ACCEPTED,
)
def change_user_info_by_himself(
    schema: user_order_s.UserChangeByUserHimself,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Change current user main information.

        Need authentication and don't need special permissions!

        Only you can change this info.

        No one else can get access.
    """
    return user_logic.change_user_by_himself(
        email=current_user.email,
        schema=schema,
        db=db,
    )

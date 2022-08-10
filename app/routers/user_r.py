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
    response_model=list[user_order_s.UserInListOfUsersShow],
    status_code=status.HTTP_200_OK,
)
def get_all_users(
    latest_first: bool = True,
    limit: int = 10,
    page: int = 1,
    email: str | None = None,
    staff: bool | None = None,
    superuser: bool | None = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.get_current_user),
):
    """
    Get all users.

        Need authentication and special permissions.

        Only a user who has ('is_staff', 'is_superuser') can get access.

    You can use query parameters to get some specific information as:
    * latest_first...   True shows list from end to start.
    * email... 'rt' shows every email that contains it
    * staff... shows 'staff' Users
    * superuser... shows 'superuser' Users
    """
    if security.check_permision(current_user, bottom_perm="is_staff"):
        return user_logic.get_all_users(
            db=db,
            limit=limit,
            page=page,
            reverse_sort=latest_first,
            find_by_email=email,
            find_staff=staff,
            find_superuser=superuser,
        )


# ---------------------------------------------------------------------------------------
# create_user
# ---------------------------------------------------------------------------------------


@router.post(
    "/users",
    response_model=user_order_s.UserFullShow,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    schema: user_order_s.UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create user.

        DON'T need authentication and special permissions.

    By default user will have permission:
    * is_staff = False
    * is_superuser = False
    """
    return user_logic.create_user(db=db, schema=schema)


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
    current_user: dict = Depends(security.get_current_user),
):
    """
    Get full information about user by email

        Need authentication and special permissions!

        Only a user who has ('is_staff', 'is_superuser') can get access.
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
    current_user: dict = Depends(security.get_current_user),
):
    """
    Change user permission by email

        Need authentication and special permissions!

        Only a user who has ('is_superuser') can get access.
    """
    if security.check_permision(current_user, bottom_perm="is_superuser"):
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
    current_user: dict = Depends(security.get_current_user),
):
    """
    Delete user by email.

        Need authentication and/or special permissions!

        If it's your own email you can delete your account.

        Also a users who has ('is_staff', 'is_superuser') can delete as well.
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
    "/users/me/",
    response_model=user_order_s.UserFullShow,
    status_code=status.HTTP_200_OK,
)
def read_current_user_info(
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.get_current_user),
):
    """
    Get full information about current user.

        Need authentication and don't need special permissions!

        Only owner can see this info.

    But users who has special permissions as ('is_staff', 'is_superuser')
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
    "/users/me/",
    response_model=user_order_s.UserFullShow,
    status_code=status.HTTP_202_ACCEPTED,
)
def change_user_info_by_himself(
    schema: user_order_s.UserChangeByUserHimself,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.get_current_user),
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

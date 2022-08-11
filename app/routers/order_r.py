from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import date

from app.models import order_m
from app.schemas import user_order_s
from app.database.dependb import get_db
from app.crud import author_category_logic, order_logic
from app.core import security

router = APIRouter(tags=["Orders"])

# ---------------------------------------------------------------------------------------
# get_all_orders
# ---------------------------------------------------------------------------------------


@router.get(
    "/orders",
    response_model=list[user_order_s.OrderFullShow],
    status_code=status.HTTP_200_OK,
)
def get_all_orders(
    db: Session = Depends(get_db),
    latest_first: bool = True,
    owner: int | None = None,
    limit: int = 10,
    page: int = 1,
    total_min: float | None = None,
    total_max: float | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    complete: bool | None = None,
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Get all orders.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.

    You can use query parameters to get some specific information as:
    * latest_first...   True shows list  from end to start
    * owner... shows User orders by his customer_id
    * total_min and total_max... shows orders using borders of total price
    * date_from and date_to... shows orders using borders of delivery date
    * complete... shows is the order completed or not


        Delivery date example ('2000-01-01' Year/month/day)
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return order_logic.get_all_orders(
            db=db,
            page=page,
            limit=limit,
            latest_first=latest_first,
            total_min=total_min,
            total_max=total_max,
            owner=owner,
            date_from=date_from,
            date_to=date_to,
            complete=complete,
        )


# ---------------------------------------------------------------------------------------
# create_order
# ---------------------------------------------------------------------------------------


@router.post(
    "/orders",
    response_model=user_order_s.OrderFullShow,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order: user_order_s.OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Create order.

        Need authentication and DON'T need special permissions.

    When you will create an order. It automaticaly add some field as:
    * total_price... auto calculating. depends by book price and quantity
    * paid... default False
    * customer... current user
    * delivery_date... default null
    * complete... default False

    The part of logic described inside "PUT /orders/{order_id}"
    """
    return order_logic.create_item(
        item=order,
        db=db,
        current_user=current_user,
    )


# ---------------------------------------------------------------------------------------
# get_order_by_id
# ---------------------------------------------------------------------------------------


@router.get(
    "/orders/{order_id}",
    response_model=user_order_s.OrderFullShow,
    status_code=status.HTTP_200_OK,
)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Get order by id.

        Need authentication and special permissions.

        Only a user who has role='staff' or role='admin' can get access.
    """

    if security.check_permision(current_user, bottom_perm="staff"):
        return author_category_logic.get_item_by_id(
            item_id=order_id,
            db=db,
            item_model=order_m.Order,
        )


# ---------------------------------------------------------------------------------------
# update_order_by_id_by_staff
# ---------------------------------------------------------------------------------------


@router.put(
    "/orders/{order_id}",
    response_model=user_order_s.OrderFullShow,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_order_by_id_by_staff(
    order_id: int,
    order: user_order_s.OrderUpdateByStaff,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Change order by id.

        Need authentication and special permissions.

        Users who has role='staff' or role='admin' can change as well.



    The logic is when the user pays for the order staff will
    change 'paid' field as True and will set a delivery_date:

        {
            "paid": "True",

            "delivery_date": "2022-01-01",

            "complete": "False"
        }

    When order is delivered staff will change 'complete'
    field as True:

        {
            "paid": "True",

            "delivery_date": "2022-01-01",

            "complete": "True"
        }

    (This is the way to improve this project, now everything doing manually)

    Date to set as

        "2000-01-01" (year, month, day)
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return order_logic.update_item_by_id_by_staff(
            item_id=order_id,
            db=db,
            schema=order,
        )


# ---------------------------------------------------------------------------------------
# delete_order_by_id
# ---------------------------------------------------------------------------------------


@router.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_200_OK,
)
def delete_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Delete order by id.

        Need authentication and special permissions.
    """
    if security.check_permision(current_user, bottom_perm="staff"):
        return author_category_logic.delete_item_by_id(
            item_id=order_id,
            db=db,
            item_model=order_m.Order,
        )


# ---------------------------------------------------------------------------------------
# update_own_last_order_by_current_user
# ---------------------------------------------------------------------------------------


@router.put(
    "/orders/my-order/",
    response_model=user_order_s.OrderFullShow,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_own_last_order_by_current_user(
    order: user_order_s.OrderUpdateByUserHimself,
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.auth_access_wrapper),
):
    """
    Change last order of current_user by himself.

        Need authentication and DON'T need special permissions.

        Only user who created it - can change it.
    """
    return order_logic.update_last_order_by_user(
        db=db,
        schema=order,
        current_user=current_user,
    )

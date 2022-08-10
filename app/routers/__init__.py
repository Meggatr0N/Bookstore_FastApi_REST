from fastapi import APIRouter

from app.routers import (
    authentication_r,
    user_r,
    author_r,
    category_r,
    book_r,
    order_r,
)

api_router = APIRouter()


api_router.include_router(authentication_r.router)
api_router.include_router(category_r.router)
api_router.include_router(author_r.router)
api_router.include_router(book_r.router)
api_router.include_router(user_r.router)
api_router.include_router(order_r.router)

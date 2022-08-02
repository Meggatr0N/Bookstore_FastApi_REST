from fastapi import APIRouter

from app.routers import authentication_r, store_r, user_r

api_router = APIRouter()


api_router.include_router(authentication_r.router)
api_router.include_router(store_r.router)
api_router.include_router(user_r.router, tags=["User"])

from fastapi import APIRouter

from app.api.v1 import store, user

api_router = APIRouter()
api_router.include_router(store.router)
api_router.include_router(user.router, tags=["User"])

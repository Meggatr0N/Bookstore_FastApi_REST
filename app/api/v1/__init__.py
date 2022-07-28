from fastapi import APIRouter

from app.api.v1 import store

api_router = APIRouter()
api_router.include_router(store.router)  # , tags=["products"])

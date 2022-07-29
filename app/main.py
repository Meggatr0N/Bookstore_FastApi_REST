from fastapi import FastAPI

from app.models import store, user
from .database.db import engine
from .core import settings
from app.api.v1 import api_router


# Create all tables in the database.
store.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)


# poetry shell
# uvicorn app.main:app --reload

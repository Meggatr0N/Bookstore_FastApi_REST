from fastapi import FastAPI

from app.database.db import engine
from app.core import settings
from app.routers import api_router
from app.database.db import Base

# creating all tables in database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)


# poetry shell
# uvicorn app.main:app --reload

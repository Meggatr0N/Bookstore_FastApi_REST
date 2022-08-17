from fastapi import FastAPI

from app.database.db import engine
from app.core import settings
from app.routers import api_router
from app.database.db import Base

# creating all tables in database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)


# poetry shell                      launch virtual enviroment
# uvicorn app.main:app --reload     launch project
# pytest -v                         launch tests
# pytest --cov                      to see how many percents of
#                                   code is coverage by tests

# create a database. here is a
# generator for all database's tables for this project
# BUT! You need to launch project and when database will be created,
# comment this 2 lines of code below
# (it will generate only if database was empty)

# from app.gen import data_generator

# data_generator()

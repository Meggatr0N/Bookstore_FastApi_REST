import pytest
from typing import Any, Generator

# from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.database.db import Base
from app.main import app

from app.database.dependb import get_db
from app.core import settings


prg_user = settings.TEST_POSTGRES_USER
prg_pswrd = settings.TEST_POSTGRES_PASSWORD
prg_server = settings.TEST_POSTGRES_SERVER
prg_db = settings.TEST_POSTGRES_DB

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{prg_user}:{prg_pswrd}@{prg_server}/{prg_db}"
)

test_engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(test_engine)  # Create the tables.
    yield app
    Base.metadata.drop_all(test_engine)


@pytest.fixture()
def db_session(app: FastAPI) -> Generator[TestSession, Any, None]:
    """
    Creates a fresh sqlalchemy session for each test that operates
    in a transaction. The transaction is rolled back at the end
    of each test ensuring a clean state.
    """

    # connect to the database
    connection = test_engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()
    # bind an individual Session to the connection
    session = TestSession(bind=connection)
    yield session  # use the session in tests.
    session.close()
    # rollback - everything that happened with the
    # Session above (including calls to commit())
    # is rolled back.
    transaction.rollback()
    # return connection to the Engine
    connection.close()


@pytest.fixture()
def client(
    app: FastAPI, db_session: TestSession
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session`
    fixture to override the `get_db` dependency that is injected
    into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield

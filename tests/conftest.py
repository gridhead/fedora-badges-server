from unittest import mock
from uuid import UUID

import psycopg
import pytest
import pytest_postgresql
from httpx import AsyncClient
from sqlalchemy import create_engine, select
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine

import badges_server.system.main
from badges_server.database.data import (
    async_session_maker,
    baseobjc,
    init_async_model,
    init_sync_model,
    sync_session_maker,
)
from badges_server.database.objs import User
from badges_server.system.auth import dep_user

# Database fixtures
# these are adapted and reused from the duffy tests

postgresql_function_proc = pytest.fixture(scope="function")(
    pytest_postgresql.factories.postgresql_proc().__wrapped__
)


@pytest.fixture
def postgresql_instance(postgresql_function_proc):
    url = URL.create(
        drivername="postgresql",
        username="postgres",
        host=postgresql_function_proc.host,
        port=postgresql_function_proc.port,
        database="badges_server",
    )
    return url


@pytest.fixture
def postgresql_db(postgresql_instance):
    async_url = postgresql_instance.set(drivername="postgresql+asyncpg")
    admin_url = postgresql_instance.set(database="postgres")

    with psycopg.connect(str(admin_url), autocommit=True) as conn, conn.cursor() as cur:
        cur.execute('CREATE DATABASE "badges_server"')
        conn.commit()

    return postgresql_instance, async_url


@pytest.fixture
def postgresql_sync_url(postgresql_db):
    return postgresql_db[0]


@pytest.fixture
def postgresql_async_url(postgresql_db):
    return postgresql_db[1]


@pytest.fixture
def db_sync_engine(postgresql_sync_url):
    """A fixture which creates a synchronous database engine."""
    db_engine = create_engine(
        url=postgresql_sync_url,
        future=True,
        echo=True,
        isolation_level="SERIALIZABLE",
    )
    return db_engine


@pytest.fixture
def db_async_engine(postgresql_async_url):
    """A fixture which creates an asynchronous database engine."""
    async_db_engine = create_async_engine(
        url=postgresql_async_url,
        future=True,
        echo=True,
        isolation_level="SERIALIZABLE",
    )
    return async_db_engine


@pytest.fixture
def db_sync_schema(db_sync_engine):
    """Synchronous fixture to install the database schema."""
    with db_sync_engine.begin():
        baseobjc.metadata.create_all(db_sync_engine)


@pytest.fixture
async def db_async_schema(db_async_engine):
    """Asynchronous fixture to install the database schema."""
    async with db_async_engine.begin() as conn:
        await conn.run_sync(baseobjc.metadata.create_all)


@pytest.fixture
def db_sync_model_initialized(db_sync_engine, db_sync_schema):
    """Fixture to initialize the synchronous DB model.

    This is used so db_sync_session is usable in tests.
    """
    init_sync_model(sync_engine=db_sync_engine)


@pytest.fixture
async def db_async_model_initialized(db_async_engine, db_async_schema):
    """Fixture to initialize the asynchronous DB model.

    This is used so db_async_session is usable in tests.
    """
    await init_async_model(db_async_engine)


@pytest.fixture
def db_sync_session(db_sync_model_initialized):
    """Fixture setting up a synchronous DB session."""
    db_session = sync_session_maker()
    try:
        yield db_session
    finally:
        db_session.close()


@pytest.fixture
async def db_async_session(db_async_model_initialized):
    """Fixture setting up an asynchronous DB session."""
    db_session = async_session_maker()
    try:
        yield db_session
    finally:
        await db_session.close()


def _test_data():
    data = set()

    testuser = User(
        username="testuser",
        mailaddr="testuser@badges.test",
        desc="",
        withdraw=False,
        headuser=False,
        uuid=UUID(hex="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").hex[0:8],
    )
    data.add(testuser)

    headuser = User(
        username="headuser",
        mailaddr="headuser@badges.test",
        desc="",
        withdraw=False,
        headuser=True,
        uuid=UUID(hex="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb").hex[0:8],
    )
    data.add(headuser)

    testuser_withdrawn = User(
        username="testuser_withdrawn",
        mailaddr="testuser_withdrawn@badges.test",
        desc="",
        withdraw=True,
        headuser=False,
        uuid=UUID(hex="cccccccccccccccccccccccccccccccc").hex[0:8],
    )
    data.add(testuser_withdrawn)

    return data


@pytest.fixture
def db_sync_test_data(db_sync_session):
    """A fixture to fill the DB with test data.

    Use this in synchronous tests.
    """
    with db_sync_session.begin():
        for obj in _test_data():
            db_sync_session.add(obj)


@pytest.fixture
async def db_async_test_data(db_async_session):
    """A fixture to fill the DB with test data.

    Use this in asynchronous tests.
    """
    async with db_async_session.begin():
        for obj in _test_data():
            db_async_session.add(obj)


@pytest.fixture
async def client(db_async_session, db_async_test_data):
    async with AsyncClient(
        app=badges_server.system.main.app, base_url="http://badges-server.example.test"
    ) as client:
        yield client


@pytest.fixture
async def authenticate_user(authenticate_user_username, db_async_session):
    user = None

    if authenticate_user_username:
        user = (
            await db_async_session.execute(
                select(User).filter_by(username=authenticate_user_username)
            )
        ).scalar_one_or_none()

    def get_user():
        return user

    with mock.patch.dict(badges_server.system.main.app.dependency_overrides):
        badges_server.system.main.app.dependency_overrides[dep_user] = get_user

        yield user

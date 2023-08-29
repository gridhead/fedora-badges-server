import psycopg
import pytest
import pytest_postgresql
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine

from badges_server.database.data import (
    async_session_maker,
    baseobjc,
    init_async_model,
    init_sync_model,
    sync_session_maker,
)
from badges_server.database.objs import User
from badges_server.system import main

# Database fixtures

# Like postgresql_proc, but scoped for test functions. This makes testing slower but ensures that
# tests don't affect each other, especially if conducted in parallel.
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

    user = User(username="testuser", mailaddr="testuser@badges.test")
    data.add(user)

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
    async with AsyncClient(app=main.app, base_url="http://badges-server.example.test") as client:
        yield client

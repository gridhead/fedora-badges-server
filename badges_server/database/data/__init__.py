import asyncio
import sys

from sqlalchemy import URL, MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from badges_server.config import logrdata, nameconv, standard

metadata = MetaData(naming_convention=nameconv)
baseobjc = declarative_base(metadata=metadata)


def get_sync_engine():
    engnloca = URL.create(
        drivername="postgresql+psycopg2",
        username=standard.username,
        password=standard.password,
        host=standard.jsyncurl,
        port=standard.dtbsport,
        database=standard.database,
    )
    try:
        engnobjc = create_engine(engnloca)
    except Exception as expt:
        engnobjc = None
        logrdata.logrobjc.error(f"Cannot create database engine - {expt}")
        sys.exit(1)
    return engnobjc


def get_async_engine():
    engnloca = URL.create(
        drivername="postgresql+asyncpg",
        username=standard.username,
        password=standard.password,
        host=standard.jsyncurl,
        port=standard.dtbsport,
        database=standard.database,
    )
    try:
        engnobjc = create_async_engine(engnloca)
    except Exception as expt:
        engnobjc = None
        logrdata.logrobjc.error(f"Cannot create database engine - {expt}")
        sys.exit(1)
    return engnobjc


sync_session_maker = sessionmaker(expire_on_commit=False, future=True)
async_session_maker = sessionmaker(class_=AsyncSession, expire_on_commit=False, future=True)


def init_sync_model(engnobjc: Engine = None):
    if not engnobjc:
        engnobjc = get_sync_engine()
    sync_session_maker.configure(bind=engnobjc)


async def init_async_model(engnobjc: AsyncEngine = None):
    if not engnobjc:
        engnobjc = get_async_engine()
    async_session_maker.configure(bind=engnobjc)


def init_model(syncengn: Engine, asyneng: Engine):
    init_sync_model(syncengn)
    asyncio.run(init_async_model(asyneng))

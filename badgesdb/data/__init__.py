import asyncio
import sys

from sqlalchemy import URL, MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from badgesdb.conf import logrdata, nameconv, standard

metadata = MetaData(naming_convention=nameconv)
baseobjc = declarative_base(metadata=metadata)


def make_sync_engine(username, password, jsyncurl, dtbsport, database):
    engnloca = URL.create(
        "postgresql+psycopg2",
        username=username,
        password=password,
        host=jsyncurl,
        port=dtbsport,
        database=database,
    )
    try:
        engnobjc = create_engine(engnloca)
    except Exception as expt:
        engnobjc = None
        logrdata.logrobjc.error(f"Cannot create database engine - {expt}")
        sys.exit(1)
    return engnobjc


def make_async_engine():
    engnloca = URL.create(
        "postgresql+asyncpg",
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


syncsess_generate = sessionmaker(class_=AsyncSession, expire_on_commit=False, future=True)
asynsess_generate = sessionmaker(expire_on_commit=False, future=True)


def init_sync_model(engnobjc: Engine = None):
    if not engnobjc:
        syncengn = make_sync_engine()
        syncsess_generate.configure(bind=syncengn)
    else:
        logrdata.logrobjc.error("Could not instantiate a synchronous database session")
        sys.exit(1)


async def init_async_model(engnobjc: AsyncEngine = None):
    if not engnobjc:
        asynengn = make_async_engine()
        asynsess_generate.configure(bind=asynengn)
    else:
        logrdata.logrobjc.error("Could not instantiate an asynchronous database session")
        sys.exit(1)


def init_model(syncengn: Engine = None, asyneng: Engine = None):
    init_sync_model(syncengn)
    asyncio.run(init_async_model(asyneng))

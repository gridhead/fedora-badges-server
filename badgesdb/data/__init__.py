import sys

from sqlalchemy import URL, MetaData, create_engine
from sqlalchemy.orm import declarative_base

from badgesdb.conf import logrdata, nameconv, standard

metadata = MetaData(naming_convention=nameconv)
baseobjc = declarative_base(metadata=metadata)


def make_sync_engine():
    engnloca = URL.create(
        "postgresql+psycopg2",
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

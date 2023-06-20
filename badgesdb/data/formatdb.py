import sys
from pathlib import Path

from alembic import command, config
from sqlalchemy import URL, inspect

from badgesdb.conf import logrdata, standard
from badgesdb.data import make_sync_engine, metadata

migrpath = str(Path(str(Path(__file__).parent.parent), str("migr")))


def make_database():
    engnobjc = make_sync_engine()
    insprslt = inspect(engnobjc)
    relation = sorted(indx for indx in metadata.tables if insprslt.has_table(indx))

    if relation:
        logrdata.logrobjc.error("Relations already available")
        logrdata.logrobjc.error(", ".join(relation))
        logrdata.logrobjc.error("Refusing to make changes to the database schema")
        sys.exit(1)

    with engnobjc.begin():
        logrdata.logrobjc.info("Creating database schema")
        metadata.create_all(bind=engnobjc)

        logrdata.logrobjc.info("Setting up database migrations")
        confobjc = config.Config()
        confobjc.set_main_option("script_location", migrpath)
        confobjc.set_main_option(
            "sqlalchemy.url",
            str(
                URL.create(
                    "postgresql+psycopg2",
                    username=standard.username,
                    password=standard.password,
                    host=standard.jsyncurl,
                    port=standard.dtbsport,
                    database=standard.database,
                )
            ),
        )
        command.stamp(confobjc, "head")
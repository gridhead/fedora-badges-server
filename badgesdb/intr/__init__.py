from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

from badgesdb.conf import logrdata
from badgesdb.data import asynsess_generate


class BadgesDB:
    def __init__(self, username, password, jsyncurl, dtbsport, database):
        self.username = username
        self.password = password
        self.jsyncurl = jsyncurl
        self.dtbspost = dtbsport
        self.database = database
        self.engnobjc = create_async_engine(
            URL.create(
                drivername="postgresql+asyncpg",
                username=self.username,
                password=self.password,
                host=self.jsyncurl,
                port=self.dtbspost,
                database=self.database,
            )
        )
        sesclass = asynsess_generate
        sesclass.configure(bind=self.engnobjc)
        self.sessobjc = sesclass()

    async def cleanall(self):
        try:
            # yield self.sessobjc
            # I DO NOT NEED A LONG-LIVING SESSION OBJECT SO I CHOSE AGAINST "YIELDING" THE SESSOBJC
            # @nilsph, CORRECT ME IF I AM MISTAKEN.
            # Reference was taken from
            # https://github.com/CentOS/duffy/blob/dev/duffy/app/database.py
            await self.sessobjc.commit()
        except Exception as expt:
            await self.sessobjc.rollback()
            logrdata.logrobjc.error(
                f"Could not perform the requested transaction on the database - {expt}"
            )
            raise
        finally:
            await self.sessobjc.close()

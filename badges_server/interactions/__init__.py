from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine


class badgesdb:
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

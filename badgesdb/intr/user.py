from sqlalchemy import select
from sqlalchemy.orm import selectinload

from badgesdb.conf import logrdata
from badgesdb.form.user import UserPeruseSole_Parameter
from badgesdb.intr import BadgesDB
from badgesdb.objs.user import User


class IntrUser(BadgesDB):
    def __init__(self, username, password, jsyncurl, dtbsport, database):
        super().__init__(
            username=username,
            password=password,
            jsyncurl=jsyncurl,
            dtbsport=dtbsport,
            database=database,
        )
        self.relaname = "USER"

    def create(self):
        pass

    async def peruse_sole(self, objciden: UserPeruseSole_Parameter):
        try:
            quryobjc = select(User).filter_by(id=objciden.id).options(selectinload("*"))
            rsltobjc = await self.sessobjc.execute(quryobjc)
            await self.cleanall()
            return rsltobjc.scalar_one_or_none()
        except Exception as expt:
            logrdata.logrobjc.error(
                f"Could not read one record from the relation {self.relaname} - {expt}"
            )
            return False

    def peruse_many(self):
        pass

    def update(self):
        pass

    def remove(self):
        pass

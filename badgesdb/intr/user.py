from sqlalchemy import select
from sqlalchemy.orm import selectinload

from badgesdb.conf import logrdata
from badgesdb.data import asynsess_generate
from badgesdb.form.user import UserPeruseSole_Parameter
from badgesdb.intr import BadgesDB
from badgesdb.objs.user import User


class IntrUser:
    def __init__(self, badgesdb: BadgesDB):
        self.relaname = "USER"
        self.sesclass = asynsess_generate
        self.sesclass.configure(bind=badgesdb.engnobjc)

    def create(self):
        pass

    async def peruse_sole(self, objciden: UserPeruseSole_Parameter):
        try:
            sessobjc = self.sesclass()
            quryobjc = select(User).filter_by(id=objciden.id).options(selectinload("*"))
            rsltobjc = await sessobjc.execute(quryobjc)
            await sessobjc.close()
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

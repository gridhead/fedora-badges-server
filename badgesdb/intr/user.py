from sqlalchemy import select
from sqlalchemy.orm import selectinload

from badgesdb.form.user import UserPeruseSole_Parameter
from badgesdb.intr import BadgesDB
from badgesdb.objs.user import User


class IntrUser:
    def __init__(self, badgesdb: BadgesDB):
        super().__init__()
        self.badgesdb = badgesdb

    def create(self):
        pass

    def peruse_sole(self, objciden: UserPeruseSole_Parameter):
        quryobjc = select(User).filter_by(id=objciden.id).options(selectinload("*"))
        rsltobjc = self.badgesdb.sessobjc.execute(quryobjc)
        return rsltobjc.scalar_one_or_none()

    def peruse_many(self):
        pass

    def update(self):
        pass

    def remove(self):
        pass

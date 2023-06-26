from sqlalchemy import select
from sqlalchemy.orm import selectinload

from badgesdb.form.user import UserPeruseSole_Parameter
from badgesdb.intr import BadgesDBSync
from badgesdb.objs.user import User


class Intr_User:
    def __init__(self, engnobjc: BadgesDBSync):
        self.engnobjc = engnobjc

    def create(self):
        pass

    def peruse_sole(self, objciden: UserPeruseSole_Parameter):
        quryobjc = select(User).filter_by(id=objciden.id).options(selectinload("*"))
        rsltobjc = self.engnobjc.syncsess.execute(quryobjc).scalar_one_or_none()
        return rsltobjc

    def peruse_many(self):
        pass

    def update(self):
        pass

    def remove(self):
        pass

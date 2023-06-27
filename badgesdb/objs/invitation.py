from sqlalchemy import Column, ForeignKey, Integer

from badgesdb.data import baseobjc
from badgesdb.objs.accolade import Accolade
from badgesdb.objs.user import User
from badgesdb.util import CreateableMixin, TZDateTime


class Invitation(baseobjc, CreateableMixin):
    __tablename__ = "invitation"
    id = Column(Integer, primary_key=True, nullable=False)
    stopdate = Column(TZDateTime, unique=False, nullable=True, default=None)
    accolade_id = Column(Integer, ForeignKey(Accolade.id), unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), unique=False, nullable=False)

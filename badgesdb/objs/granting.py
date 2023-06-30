from sqlalchemy import Column, ForeignKey, Integer, UnicodeText

from badgesdb.data import baseobjc
from badgesdb.objs.accolade import Accolade
from badgesdb.objs.user import User
from badgesdb.util import CreateableMixin


class Granting(baseobjc, CreateableMixin):
    __tablename__ = "granting"
    id = Column(Integer, primary_key=True, nullable=False)
    accolade_id = Column(Integer, ForeignKey(Accolade.id), unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), unique=False, nullable=False)
    reason = Column(UnicodeText, unique=False, nullable=False)

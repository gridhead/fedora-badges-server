from sqlalchemy import Column, ForeignKey, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.objs.accolade import Accolade
from badges_server.database.objs.user import User
from badges_server.database.util import CreateableMixin, UUIDCreateableMixin


class Granting(baseobjc, CreateableMixin, UUIDCreateableMixin):
    __tablename__ = "granting"
    id = Column(Integer, primary_key=True, nullable=False)
    accolade_id = Column(Integer, ForeignKey(Accolade.id), unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), unique=False, nullable=False)
    reason = Column(UnicodeText, unique=False, nullable=False)

from sqlalchemy import Column, ForeignKey, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.objs.accolade import Accolade
from badges_server.database.objs.user import User
from badges_server.database.util import CreateableMixin, TZDateTime, UUIDCreateableMixin


class Invitation(baseobjc, CreateableMixin, UUIDCreateableMixin):
    __tablename__ = "invitation"
    id = Column(Integer, primary_key=True, nullable=False)
    stopdate = Column(TZDateTime, unique=False, nullable=True, default=None)
    accolade_id = Column(Integer, ForeignKey(Accolade.id), unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), unique=False, nullable=False)
    code = Column(UnicodeText, unique=True, nullable=False)

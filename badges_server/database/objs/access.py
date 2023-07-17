from sqlalchemy import Boolean, Column, ForeignKey, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.objs.user import User
from badges_server.database.util import CreateableMixin, TZDateTime, UUIDCreateableMixin


class Access(baseobjc, CreateableMixin, UUIDCreateableMixin):
    __tablename__ = "access"
    id = Column("id", Integer, primary_key=True, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey(User.id), unique=False, nullable=False)
    stopdate = Column("stopdate", TZDateTime, unique=False, nullable=True, default=None)
    code = Column("code", UnicodeText, unique=True, nullable=False)
    active = Column("active", Boolean, unique=False, nullable=False)

from sqlalchemy import Column, ForeignKey, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.objs.user import User
from badges_server.database.util import CreateableMixin


class Access(baseobjc, CreateableMixin):
    __tablename__ = "access"
    id = Column("id", Integer, primary_key=True, nullable=False)
    name = Column("name", UnicodeText, unique=False, nullable=False)
    description = Column("description", UnicodeText, unique=False, nullable=True, default=True)
    user_id = Column("user_id", Integer, ForeignKey(User.id), unique=False, nullable=False)
    code = Column("code", UnicodeText, unique=True, nullable=False)

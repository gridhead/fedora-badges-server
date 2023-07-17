from sqlalchemy import Boolean, Column, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.util import CreateableMixin, UUIDCreateableMixin


class Type(baseobjc, UUIDCreateableMixin, CreateableMixin):
    __tablename__ = "type"
    id = Column("id", Integer, primary_key=True, nullable=False)
    name = Column("name", UnicodeText, unique=False, nullable=False)
    desc = Column("desc", UnicodeText, unique=False, nullable=True, default=None)
    arranged = Column("arranged", Boolean, unique=False, nullable=False)

from sqlalchemy import Boolean, Column, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.util import CreateableMixin, UUIDCreateableMixin


class Type(baseobjc, UUIDCreateableMixin, CreateableMixin):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, unique=False, nullable=False)
    description = Column(UnicodeText, unique=False, nullable=True, default=None)
    arranged = Column(Boolean, unique=False, nullable=False)

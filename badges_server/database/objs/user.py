from sqlalchemy import Boolean, Column, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.util import TZDateTime, UserCreateableMixin


class User(baseobjc, UserCreateableMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    mailaddr = Column(UnicodeText, unique=False, nullable=False)
    username = Column(UnicodeText, unique=True, nullable=False)
    desc = Column(UnicodeText, unique=False, nullable=True, default=None)
    lastseen = Column(TZDateTime, unique=False, nullable=True, default=None)
    withdraw = Column(Boolean, unique=False, nullable=False, default=False)

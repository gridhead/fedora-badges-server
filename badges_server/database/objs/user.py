from sqlalchemy import Boolean, Column, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.util import CreateableMixin, UserCreateableMixin, UUIDCreateableMixin


class User(baseobjc, CreateableMixin, UUIDCreateableMixin, UserCreateableMixin):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=True, nullable=False)
    mailaddr = Column("mailaddr", UnicodeText, unique=False, nullable=False)
    username = Column("username", UnicodeText, unique=True, nullable=False)
    desc = Column("desc", UnicodeText, unique=False, nullable=True, default=None)
    withdraw = Column("withdraw", Boolean, unique=False, nullable=False, default=False)
    headuser = Column("headuser", Boolean, unique=False, nullable=False, default=False)

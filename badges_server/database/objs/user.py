from sqlalchemy import Boolean, Column, Integer, UnicodeText
from sqlalchemy.orm import relationship

from badges_server.database.data import baseobjc
from badges_server.database.objs.access import Access
from badges_server.database.objs.granting import Granting
from badges_server.database.objs.invitation import Invitation
from badges_server.database.objs.provider import Provider
from badges_server.database.util import CreateableMixin, UserCreateableMixin, UUIDCreateableMixin


class User(baseobjc, CreateableMixin, UUIDCreateableMixin, UserCreateableMixin):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=True, nullable=False)
    mailaddr = Column("mailaddr", UnicodeText, unique=False, nullable=False)
    username = Column("username", UnicodeText, unique=True, nullable=False)
    desc = Column("desc", UnicodeText, unique=False, nullable=True, default=None)
    withdraw = Column("withdraw", Boolean, unique=False, nullable=False, default=False)
    headuser = Column("headuser", Boolean, unique=False, nullable=False, default=False)
    access = relationship(Access, backref="type", passive_deletes=True)
    granting = relationship(Granting, backref="type", passive_deletes=True)
    invitation = relationship(Invitation, backref="type", passive_deletes=True)
    provider = relationship(Provider, backref="type", passive_deletes=True)

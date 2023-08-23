from sqlalchemy import Column, ForeignKey, Integer, UnicodeText
from sqlalchemy.orm import relationship

from badges_server.database.data import baseobjc
from badges_server.database.objs.granting import Granting
from badges_server.database.objs.invitation import Invitation
from badges_server.database.objs.provider import Provider
from badges_server.database.util import CreateableMixin, UUIDCreateableMixin


class Accolade(baseobjc, CreateableMixin, UUIDCreateableMixin):
    __tablename__ = "accolade"
    id = Column("id", Integer, primary_key=True, nullable=False)
    name = Column("name", UnicodeText, unique=True, nullable=False)
    desc = Column("desc", UnicodeText, unique=False, nullable=True, default=None)
    imageurl = Column("imageurl", UnicodeText, unique=False, nullable=False)
    criteria = Column("criteria", UnicodeText, unique=False, nullable=True, default=None)
    type_id = Column("type_id", Integer, ForeignKey("type.id", ondelete="CASCADE"), unique=False)
    sequence = Column("sequence", Integer, unique=False, nullable=True, default=None)
    tags = Column("tags", UnicodeText, unique=False, nullable=True, default=None)
    granting = relationship(Granting, backref="accolade", passive_deletes=True)
    invitation = relationship(Invitation, backref="accolade", passive_deletes=True)
    provider = relationship(Provider, backref="accolade", passive_deletes=True)

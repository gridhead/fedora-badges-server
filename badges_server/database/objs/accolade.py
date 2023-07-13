from sqlalchemy import Column, ForeignKey, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.objs.type import Type
from badges_server.database.util import CreateableMixin, UUIDCreateableMixin


class Accolade(baseobjc, CreateableMixin, UUIDCreateableMixin):
    __tablename__ = "accolade"
    id = Column("id", Integer, primary_key=True, nullable=False)
    name = Column("name", UnicodeText, unique=True, nullable=False)
    desc = Column("desc", UnicodeText, unique=False, nullable=True, default=None)
    imageurl = Column("imageurl", UnicodeText, unique=False, nullable=False)
    criteria = Column("criteria", UnicodeText, unique=False, nullable=True, default=None)
    type_id = Column("type_id", Integer, ForeignKey(Type.id), unique=False)
    sequence = Column("sequence", Integer, unique=False, nullable=True, default=None)
    tags = Column("tags", UnicodeText, unique=False, nullable=True, default=None)

from sqlalchemy import Column, ForeignKey, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.objs.type import Type
from badges_server.util import CreateableMixin


class Accolade(baseobjc, CreateableMixin):
    __tablename__ = "accolade"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, unique=True, nullable=False)
    description = Column(UnicodeText, unique=False, nullable=True, default=None)
    imageurl = Column(UnicodeText, unique=False, nullable=False)
    origrqst = Column(UnicodeText, unique=False, nullable=True, default=None)
    type_id = Column(Integer, ForeignKey(Type.id), unique=False)
    sequence = Column(Integer, unique=False, nullable=True, default=None)
    tags = Column(UnicodeText, unique=False, nullable=True, default=None)

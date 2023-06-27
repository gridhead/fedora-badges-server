from sqlalchemy import Column, ForeignKey, Integer, UnicodeText

from badgesdb.data import baseobjc
from badgesdb.objs.type import Type
from badgesdb.util import CreateableMixin


class Accolade(baseobjc, CreateableMixin):
    __tablename__ = "accolade"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, unique=True, nullable=False)
    desc = Column(UnicodeText, unique=False, nullable=True, default=None)
    imageurl = Column(UnicodeText, unique=False, nullable=False)
    origrqst = Column(UnicodeText, unique=False, nullable=True, default=None)
    type_id = Column(Integer, ForeignKey(Type.id), unique=False)
    sequence = Column(Integer, unique=False, nullable=True, default=None)
    tags = Column(UnicodeText, unique=False, nullable=True, default=None)

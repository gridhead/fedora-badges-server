from sqlalchemy import Column, ForeignKey, Integer, Time, UnicodeText

from badgesdb.data import baseobjc
from badgesdb.objs.type import Type


class Accolade(baseobjc):
    __tablename__ = "accolade"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, unique=True, nullable=False)
    desc = Column(UnicodeText, unique=False, nullable=True)
    imageurl = Column(UnicodeText, unique=False, nullable=False)
    origrqst = Column(UnicodeText, unique=False, nullable=True)
    makedate = Column(Time, unique=False, nullable=False)
    type_id = Column(Integer, ForeignKey(Type.id), unique=False, nullable=False)
    sequence = Column(Integer, unique=False, nullable=True)
    tags = Column(UnicodeText, unique=False, nullable=True)

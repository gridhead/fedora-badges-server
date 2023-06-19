from sqlalchemy import BLOB, Column, ForeignKey, Integer, Time, UnicodeText

from badgesdb.objs.type import Type


class Accolade:
    __tablename__ = "accolade"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, unique=True, nullable=False)
    view = Column(BLOB, unique=False, nullable=False)
    desc = Column(UnicodeText, unique=False, nullable=True)
    origrqst = Column(UnicodeText, unique=False, nullable=True)
    makedate = Column(Time, unique=False, nullable=False)
    type_id = Column(Integer, ForeignKey(Type.id), unique=False, nullable=False)
    sequence = Column(Integer, unique=False, nullable=True)
    tags = Column(UnicodeText, unique=False, nullable=True)

from sqlalchemy import Column, ForeignKey, Integer, Time

from badgesdb.objs.accolade import Accolade
from badgesdb.objs.user import User


class Invitation:
    __tablename__ = "invitation"
    id = Column(Integer, primary_key=True, nullable=False)
    makedate = Column(Time, unique=False, nullable=False)
    stopdate = Column(Time, unique=False, nullable=False)
    accolade_id = Column(Integer, ForeignKey(Accolade.id), unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), unique=False, nullable=False)

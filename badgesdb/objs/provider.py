from sqlalchemy import Column, ForeignKey, Integer

from badgesdb.objs.accolade import Accolade
from badgesdb.objs.user import User


class Provider:
    __tablename__ = "provider"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    accolade_id = Column(Integer, ForeignKey(Accolade.id), nullable=False)

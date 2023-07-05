from sqlalchemy import Column, ForeignKey, Integer

from badges_server.database.data import baseobjc
from badges_server.database.objs.accolade import Accolade
from badges_server.database.objs.user import User


class Provider(baseobjc):
    __tablename__ = "provider"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    accolade_id = Column(Integer, ForeignKey(Accolade.id), nullable=False)

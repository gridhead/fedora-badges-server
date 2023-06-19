from sqlalchemy import Boolean, Column, Integer, Time, UnicodeText


class User:
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    mailaddr = Column(UnicodeText, unique=False, nullable=False)
    username = Column(UnicodeText, unique=True, nullable=False)
    desc = Column(UnicodeText, unique=False, nullable=True)
    makedate = Column(Time, unique=False, nullable=False)
    lastseen = Column(Time, unique=False, nullable=False)
    withdraw = Column(Boolean, unique=False, nullable=False)
    rank = Column(Integer, unique=False, nullable=False)

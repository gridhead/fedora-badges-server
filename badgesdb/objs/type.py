from sqlalchemy import Boolean, Column, Integer, UnicodeText


class Type:
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(UnicodeText, unique=False, nullable=False)
    desc = Column(UnicodeText, unique=False, nullable=True)
    arranged = Column(Boolean, unique=False, nullable=False)

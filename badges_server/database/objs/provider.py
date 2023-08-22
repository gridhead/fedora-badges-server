from sqlalchemy import Column, ForeignKey, Integer

from badges_server.database.data import baseobjc


class Provider(baseobjc):
    __tablename__ = "provider"
    id = Column("id", Integer, primary_key=True, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    accolade_id = Column(
        "accolade_id", Integer, ForeignKey("accolade.id", ondelete="CASCADE"), nullable=False
    )

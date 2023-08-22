from sqlalchemy import Column, ForeignKey, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.util import CreateableMixin, UUIDCreateableMixin


class Granting(baseobjc, CreateableMixin, UUIDCreateableMixin):
    __tablename__ = "granting"
    id = Column("id", Integer, primary_key=True, nullable=False)
    accolade_id = Column(
        "accolade_id",
        Integer,
        ForeignKey("accolade.id", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )
    user_id = Column(
        "user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=False, nullable=False
    )
    reason = Column("reason", UnicodeText, unique=False, nullable=False)

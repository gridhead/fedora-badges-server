from sqlalchemy import Boolean, Column, ForeignKey, Integer, UnicodeText

from badges_server.database.data import baseobjc
from badges_server.database.util import CreateableMixin, TZDateTime, UUIDCreateableMixin


class Invitation(baseobjc, CreateableMixin, UUIDCreateableMixin):
    __tablename__ = "invitation"
    id = Column("id", Integer, primary_key=True, nullable=False)
    stopdate = Column("stopdate", TZDateTime, unique=False, nullable=True, default=None)
    accolade_id = Column(
        "accolade_id",
        Integer,
        ForeignKey("accolade.id", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )
    active = Column("active", Boolean, unique=False, nullable=False)
    user_id = Column(
        "user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=False, nullable=False
    )
    code = Column("code", UnicodeText, unique=True, nullable=False)

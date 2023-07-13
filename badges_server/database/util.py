import datetime

from sqlalchemy import Column, Integer, UnicodeText
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import DateTime as sqlDateTime
from sqlalchemy.types import TypeDecorator


class TZDateTime(TypeDecorator):
    """
    The TZDateTime class is taken from
    https://docs.sqlalchemy.org/en/14/core/custom_types.html#store-timezone-aware-timestamps-as-timezone-naive-utc
    """

    impl = sqlDateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo:
                raise TypeError("tzinfo is required")
            value = value.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value


class utcnow(FunctionElement):
    """
    Current timestamp in UTC for SQL expressions.
    """

    type = sqlDateTime
    inherit_cache = True


@compiles(utcnow, "postgresql")
def _postgresql_utcnow(element, compiler, **kwargs):
    return "(NOW() AT TIME ZONE 'utc')"


class CreateableMixin:
    """
    An SQLAlchemy mixin to store the time when a thing was created.

    With an asynchronous session this may need to eagerly load the
    default created_at value upon INSERT, e.g. when the attribute is
    accessed on validation of a Pydantic model. This can be achieved by
    setting __mapper_args__ = {"eager_defaults": True}.
    """

    makedate = Column(TZDateTime, nullable=False, server_default=utcnow())


class UserCreateableMixin:
    """
    An SQLAlchemy mixin to calculate the current user's rank

    TODO - Ranks should be unique to one person - So unique must be set to True.
    TODO - Default should be calculated after going through the existing users.
    """

    rank = Column(Integer, unique=False, nullable=False, default=0)


class UUIDCreateableMixin:
    """
    An SQLAlchemy mixin to automatically generate a custom 8-digit UUID string
    """

    uuid = Column(UnicodeText, unique=True, nullable=False)

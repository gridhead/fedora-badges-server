from abc import ABC
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserCreateableMixin(BaseModel):
    """
    Mixin for obtaining the current datetime
    """

    makedate: datetime


class UserBase(BaseModel, ABC):
    """
    Base: User
    """

    id: Optional[int]
    mailaddr: Optional[str]
    username: Optional[str]
    desc: Optional[str]
    makedate: Optional[datetime]
    lastseen: Optional[datetime]
    withdraw: Optional[bool]
    rank: Optional[int]


class UserCreate_Parameter(UserBase, UserCreateableMixin):
    """
    Expected parameter type for the function intr.user.create
    """

    mailaddr: str
    username: str
    desc: Optional[str] = None
    withdraw: Optional[bool] = False


class UserCreate_Return(UserBase):
    """
    Expected return type for the function intr.user.create
    """

    id: int


class UserPeruseSole_Parameter(UserBase):
    """
    Expected parameter type for the function intr.user.peruse_sole
    """

    id: int


class UserPeruseSole_Return(UserBase):
    """
    Expected return type for the function intr.user.peruse_sole
    """

    id: int
    mailaddr: str
    username: str
    desc: str
    makedate: datetime
    lastseen: datetime
    withdraw: bool
    rank: int


class UserPeruseMany_Parameter(UserBase):
    """
    Expected parameter type for the function intr.user.peruse_many
    """


class UserPeruseMany_Return(UserBase):
    """
    Expected return type for the function intr.user.peruse_many
    """

    file: List[UserPeruseSole_Return]


class UserUpdate_Parameter(UserBase):
    """
    Expected parameter type for the function intr.user.update
    """

    id: int


class UserUpdate_Return(UserBase):
    """
    Expected return type for the function intr.user.update
    """

    id: int


class UserRemove_Parameter(UserBase):
    """
    Expected parameter type for the function intr.user.remove
    """

    id: int


class UserRemove_Return(UserBase):
    """
    Expected return type for the function intr.user.remove
    """

    id: int

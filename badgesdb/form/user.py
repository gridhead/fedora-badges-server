from abc import ABC
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from . import UserCreateableMixin


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


class UserCreate(UserBase, UserCreateableMixin):
    """
    Expected parameter type for the function intr.user.create
    """

    mailaddr: str
    username: str
    desc: Optional[str]
    withdraw: Optional[bool]


class UserPeruseSole(UserBase):
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


class UserPeruseMany(UserBase):
    """
    Expected return type for the function intr.user.peruse_many
    """

    file: List[UserPeruseSole]


class UserUpdate(UserBase):
    """
    Expected parameter type for the function intr.user.update
    """

    id: int


class UserRemove(UserBase):
    """
    Expected parameter type for the function intr.user.remove
    """

    id: int

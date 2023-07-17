from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from badges_server.system.common import APIResult, CreateableMixin, UUIDCreateableMixin


class UserBase(BaseModel, ABC):
    """
    Base: User
    """

    class Config:
        orm_mode = True

    id: Optional[int]
    mailaddr: Optional[str]
    username: Optional[str]
    description: Optional[str]
    lastseen: Optional[datetime]
    withdraw: Optional[bool]
    headuser: Optional[bool]
    makedate: Optional[datetime]
    uuid: Optional[str]
    rank: Optional[int]


class UserModel(UserBase, CreateableMixin, UUIDCreateableMixin):
    mailaddr: str
    username: str


class UserResult(APIResult):
    user: UserModel


class UserCreateModel(UserModel):
    pass
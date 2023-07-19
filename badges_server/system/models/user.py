from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from badges_server.system.common import APIResult


class UserBase(BaseModel, ABC):
    """
    Base: User
    """

    class Config:
        orm_mode = True

    id: Optional[int]
    mailaddr: Optional[str]
    username: Optional[str]
    desc: Optional[str]
    lastseen: Optional[datetime]
    withdraw: Optional[bool]
    headuser: Optional[bool]
    makedate: Optional[datetime]
    uuid: Optional[str]
    rank: Optional[int]


class UserModel(UserBase):
    mailaddr: str
    username: str


class UserResult(APIResult):
    user: UserModel


class UserCreateModel(UserModel):
    pass


class UserChangeDescriptionModel(BaseModel):
    uuid: str
    desc: str


class UserChangeEmailAddressModel(BaseModel):
    uuid: str
    mailaddr: str

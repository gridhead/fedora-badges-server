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


class UserModelExternal(UserBase):
    mailaddr: Optional[str]
    username: Optional[str]
    desc: Optional[str]
    lastseen: Optional[datetime]
    withdraw: Optional[bool]
    headuser: Optional[bool]
    makedate: Optional[datetime]
    uuid: Optional[str]
    rank: Optional[int]


class UserModelInternal(UserModelExternal):
    id: Optional[int]


class UserResult(APIResult):
    user: UserModelExternal


class UserCreateModel(BaseModel):
    mailaddr: str
    username: str
    desc: Optional[str]


class UserUpdatePermissionModel(BaseModel):
    uuid: str
    head: bool


class UserUpdateActivityModel(BaseModel):
    uuid: str
    withdraw: bool


class UserUpdateDescriptionModel(BaseModel):
    uuid: str
    desc: str


class UserUpdateEmailAddressModel(BaseModel):
    uuid: str
    mailaddr: str

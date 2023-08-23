from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from badges_server.system.common import APIResult


class AccoladeBase(BaseModel, ABC):
    """
    Base: Accolade
    """

    class Config:
        orm_mode = True


class AccoladeModelExternal(AccoladeBase):
    name: Optional[str]
    desc: Optional[str]
    imageurl: Optional[str]
    criteria: Optional[str]
    sequence: Optional[int] = 0
    tags: Optional[str]
    makedate: Optional[datetime]
    uuid: Optional[str]


class AccoladeModelInternal(AccoladeModelExternal):
    id: Optional[int]


class AccoladeResult(APIResult):
    user: AccoladeModelExternal


class AccoladeCreateModel(BaseModel):
    name: str
    desc: Optional[str]
    criteria: Optional[str]
    sequence: Optional[int] = 0
    type_uuid: str
    tags: Optional[str]
    uuid: Optional[str]


"""
class AccoladeUpdatePermissionModel(BaseModel):
    uuid: str
    head: bool


class AccoladeUpdateActivityModel(BaseModel):
    uuid: str
    withdraw: bool


class AccoladeUpdateDescriptionModel(BaseModel):
    uuid: str
    desc: str


class AccoladeUpdateEmailAddressModel(BaseModel):
    uuid: str
    mailaddr: str
"""

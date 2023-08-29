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
    accolade: AccoladeModelExternal
from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from badges_server.system.common import APIResult


class AccessBase(BaseModel, ABC):
    """
    Base: Access
    """

    class Config:
        orm_mode = True

    id: Optional[int]
    user_id: Optional[int]
    stopdate: Optional[datetime]
    code: Optional[str]
    active: Optional[bool]
    makedate: Optional[datetime]
    uuid: Optional[str]


class AccessModel(AccessBase):
    code: str
    makedate: datetime
    uuid: str


class AccessResult(APIResult):
    access: AccessModel

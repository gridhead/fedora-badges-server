from abc import ABC
from typing import Optional

from pydantic import BaseModel

from badges_server.system.common import APIResult


class TypeBase(BaseModel, ABC):
    """
    Base: Type
    """

    class Config:
        orm_mode = True


class TypeModelExternal(TypeBase):
    name: Optional[str]
    desc: Optional[str]
    arranged: Optional[bool]
    uuid: Optional[str]


class TypeModelInternal(TypeBase):
    id: Optional[int]


class TypeModel(TypeBase):
    name: str
    desc: str
    arranged: bool
    uuid: str


class TypeCreateModel(BaseModel):
    name: str
    desc: Optional[str]
    arranged: bool = False


class TypeUpdateNameModel(BaseModel):
    uuid: str
    name: str


class TypeResult(APIResult):
    type: TypeModel

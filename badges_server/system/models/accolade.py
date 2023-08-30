from abc import ABC
from datetime import datetime
from typing import List, Optional

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


class AccoladeSingleTypeSearchResult(BaseModel):
    quantity: int = 0
    result: List[AccoladeModelExternal] = []


class AccoladeSearchResult(APIResult):
    quantity: int = 0
    match_name: AccoladeSingleTypeSearchResult = AccoladeSingleTypeSearchResult()
    match_desc: AccoladeSingleTypeSearchResult = AccoladeSingleTypeSearchResult()
    match_tags: AccoladeSingleTypeSearchResult = AccoladeSingleTypeSearchResult()


class AccoladeUpdateNameModel(BaseModel):
    uuid: str
    name: str

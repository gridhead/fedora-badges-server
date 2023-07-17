from abc import ABC
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CreateableMixin(BaseModel):
    makedate: datetime
    lastseen: datetime
    withdraw = False
    headuser = False


class UUIDCreateableMixin(BaseModel):
    uuid: str


class APIResultAction(str, Enum):
    get = "get"
    post = "post"
    put = "put"


class APIResult(BaseModel, ABC):
    action: Optional[APIResultAction]

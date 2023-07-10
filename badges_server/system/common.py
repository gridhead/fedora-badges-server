from enum import Enum
from typing import Optional
from pydantic import BaseModel
from abc import ABC


class APIResultAction(str, Enum):
    get = "get"
    post = "post"
    put = "put"


class APIResult(BaseModel, ABC):
    action: Optional[APIResultAction]

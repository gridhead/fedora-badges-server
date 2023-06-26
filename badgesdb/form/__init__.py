from datetime import datetime

from pydantic import BaseModel


class UserCreateableMixin(BaseModel):
    makedate: datetime

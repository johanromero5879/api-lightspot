from datetime import datetime

from pydantic import EmailStr, Field

from app.common.domain import Entity, ValueId
from app.role.domain import BaseRole


class BaseUser(Entity):
    fullname: str
    email: str


class UserIn(BaseUser):
    fullname: str = Field(min_length=2, max_length=50)
    email: EmailStr
    role: ValueId
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserOut(BaseUser):
    id: ValueId = Field(alias="_id")
    role: BaseRole | str


class UserList(Entity):
    total: int
    users: list[UserOut]

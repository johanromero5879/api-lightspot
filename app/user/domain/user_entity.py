from pydantic import EmailStr, Field

from app.common.domain import Entity, ValueId
from app.role.domain import BaseRole


class BaseUser(Entity):
    fullname: str
    email: str


class UserIn(BaseUser):
    email: EmailStr


class UserOut(BaseUser):
    id: ValueId = Field(alias="_id")
    role: BaseRole | str


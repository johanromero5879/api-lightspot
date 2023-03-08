from pydantic import Field

from app.common.domain import ValueId, Entity


class BaseAuth(Entity):
    email: str
    password: str


class AuthIn(BaseAuth):
    pass


class AuthOut(Entity):
    id: ValueId = Field(alias="_id")
    password: str

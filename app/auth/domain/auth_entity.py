from pydantic import Field

from app.common.domain import ValueId, Entity


class BaseAuth(Entity):
    email: str
    password: str


class AuthIn(BaseAuth):
    pass


class AuthOut(BaseAuth):
    id: ValueId = Field(alias="_id")

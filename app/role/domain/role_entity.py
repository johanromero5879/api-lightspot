from pydantic import Field

from app.common.domain import Entity, ValueId


class BaseRole(Entity):
    name: str
    permissions: list[str]


class RoleOut(BaseRole):
    id: ValueId = Field(alias="_id")

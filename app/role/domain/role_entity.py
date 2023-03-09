from typing import TypedDict

from pydantic import Field

from app.common.domain import Entity, ValueId


class RoleDict(TypedDict):
    name: str
    permissions: list[str]


class BaseRole(Entity):
    name: str
    permissions: list[str]


class RoleIn(BaseRole):
    pass


class RoleOut(BaseRole):
    id: ValueId = Field(alias="_id")

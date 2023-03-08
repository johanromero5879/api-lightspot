from typing import TypedDict

from pydantic import Field

from app.common.domain import Entity, ValueId


class RoleDict(TypedDict):
    name: str
    permissions: list[str]


class RoleIn(Entity):
    name: str
    permissions: list[str]


class RoleOut(RoleIn):
    id: ValueId = Field(alias="_id")

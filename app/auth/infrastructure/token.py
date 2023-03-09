from pydantic import BaseModel

from app.common.domain import Entity, ValueId


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(Entity):
    user_id: ValueId | None

from pydantic import BaseModel
from bson import ObjectId


class Entity(BaseModel):
    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}

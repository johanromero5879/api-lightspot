from pymongo import MongoClient
from bson import ObjectId

from app.common.infrastructure import MongoAdapter
from app.role.domain import RoleRepository, RoleDict, RoleOut


class MongoRoleRepository(MongoAdapter, RoleRepository):
    def __init__(self, client: MongoClient | None = None):
        super().__init__("roles", client)

    def find_all(self) -> list[RoleOut]:
        roles = self.collection.find()

        return [RoleOut(**role) for role in roles]

    def find_by_name(self, name: str) -> RoleOut | None:
        role = self.collection.find_one({"name": name})
        if role:
            return RoleOut(**role)

    def insert_many(self, roles: list[RoleDict]):
        self.collection.insert_many(roles)

    def replace_permissions(self, id: ObjectId, permissions: list[str]):
        self.collection.update_one(
            {"_id": id},
            {"$set": {"permissions": permissions}}
        )

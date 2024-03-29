from pymongo import MongoClient, ASCENDING

from app.common.infrastructure import MongoAdapter
from app.role.domain import RoleRepository, BaseRole, RoleOut


class MongoRoleRepository(MongoAdapter, RoleRepository):
    def __init__(self, client: MongoClient | None = None):
        super().__init__("roles", client)

    def find_all(self) -> list[RoleOut]:
        roles = self.collection.find().sort("name", ASCENDING)

        return [RoleOut(**role) for role in roles]

    def find_by_name(self, name: str) -> RoleOut | None:
        role = self.collection.find_one({"name": name})
        if role:
            return RoleOut(**role)

    def exists_by_name(self, name: str) -> bool:
        role = self.collection.find_one({"name": name})
        return bool(role)

    def insert_many(self, roles: list[BaseRole]):
        self.collection.insert_many(
            [role.dict() for role in roles]
        )

    def insert_one(self, role: BaseRole):
        self.collection.insert_one(role.dict())

    def replace_permissions(self, name: str, permissions: list[str]):
        self.collection.update_one(
            {"name": name},
            {"$set": {"permissions": permissions}}
        )

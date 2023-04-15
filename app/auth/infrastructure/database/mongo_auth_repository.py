from pymongo import MongoClient
from bson import ObjectId

from app.auth.domain import AuthRepository, AuthOut
from app.common.infrastructure import MongoAdapter


class MongoAuthRepository(MongoAdapter, AuthRepository):
    __project = {
        "_id": 1,
        "email": 1,
        "password": 1
    }

    def __init__(self, client: MongoClient | None = None):
        super().__init__("users", client)

    def find_by_email(self, email: str) -> AuthOut | None:
        user_found = self.collection.find_one(
            {"email": email},
            self.__project
        )

        if user_found:
            return AuthOut(**user_found)

    def find_by_id(self, user_id: ObjectId) -> AuthOut | None:
        user_found = self.collection.find_one(
            {"_id": user_id},
            self.__project
        )

        if user_found:
            return AuthOut(**user_found)

    def exists_by_email(self, email: str) -> bool:
        user_found = self.collection.find_one(
            {"email": email},
            {"_id": 1}
        )

        return bool(user_found)

    def set_password(self, user_id: ObjectId, password: str) -> bool:
        result = self.collection.update_one(
            filter={"_id": user_id},
            update={"$set": {"password": password}}
        )

        return result.modified_count > 0

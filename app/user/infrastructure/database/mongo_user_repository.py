from pymongo import MongoClient
from bson import ObjectId

from app.common.infrastructure import MongoAdapter
from app.user.domain import UserRepository, UserOut


class MongoUserRepository(MongoAdapter, UserRepository):
    __project = {
        "password": 0
    }

    __lookup_role = {
        "from": "roles",
        "localField": "role",
        "foreignField": "_id",
        "as": "role",
        "pipeline": [
            {
                "$project": {"name": 1}
            }
        ]
    }

    __unwind_role = {
        "path": "$role"
    }

    def __init__(self, client: MongoClient | None = None):
        super().__init__("users", client)

    def find_by_id(self, id: ObjectId) -> UserOut | None:

        result = self.collection.aggregate([
            {"$match": {"_id": id}},
            {"$limit": 1},
            {"$project": self.__project},
            {"$lookup": self.__lookup_role},
            {"$unwind": self.__unwind_role}
        ])

        user = result.next()

        if user:
            user["role"] = user["role"]["name"]
            return UserOut(**user)

    def exists_by_id(self, id: ObjectId) -> bool:
        user = self.collection.find_one(
            {"_id": id},
            {"_id": 1}
        )

        return bool(user)

from pymongo import MongoClient, DESCENDING
from bson import ObjectId

from app.common.infrastructure import MongoAdapter
from app.user.domain import UserRepository, UserOut, UserIn, UserList


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
                "$project": {"_id": 0}
            }
        ]
    }

    __unwind_role = {
        "path": "$role"
    }

    def __init__(self, client: MongoClient | None = None):
        super().__init__("users", client)

    def find_by_id(self, id: ObjectId, has_role: bool = False) -> UserOut | None:

        result = self.collection.aggregate([
            {"$match": {"_id": id}},
            {"$limit": 1},
            {"$project": self.__project},
            {"$lookup": self.__lookup_role},
            {"$unwind": self.__unwind_role}
        ])

        user = result.next()

        if user:
            if not has_role:
                user["role"] = user["role"]["name"]

            return UserOut(**user)

    def find_all(self, limit: int, skip: int, has_role: bool = False) -> UserList:
        total = self.collection.estimated_document_count()
        result = self.collection.aggregate([
            {"$sort": {"created_at": DESCENDING}},
            {"$skip": skip},
            {"$limit": limit},
            {"$project": self.__project},
            {"$lookup": self.__lookup_role},
            {"$unwind": self.__unwind_role}
        ])

        users = []

        for user in result:
            if not has_role:
                user["role"] = user["role"]["name"]

            users.append(UserOut(**user))

        return UserList(
            total=total,
            users=users
        )

    def exists_by_id(self, id: ObjectId) -> bool:
        user = self.collection.find_one(
            {"_id": id},
            {"_id": 1}
        )

        return bool(user)

    def exists_by_email(self, email: str) -> bool:
        user = self.collection.find_one(
            {"email": email},
            {"_id": 1}
        )

        return bool(user)

    def insert_one(self, user: UserIn) -> UserOut:
        result = self.collection.insert_one(user.dict())

        return self.find_by_id(result.inserted_id, has_role=True)

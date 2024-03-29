from abc import ABC, abstractmethod

from app.common.domain import ValueId
from app.user.domain import UserOut, UserIn, UserList


class UserRepository(ABC):
    @abstractmethod
    def find_all(self, limit: int, skip: int, has_role: bool = False) -> UserList:
        pass

    @abstractmethod
    def find_by_id(self, id: ValueId, has_role: bool = False) -> UserOut | None:
        pass

    @abstractmethod
    def exists_by_id(self, id: ValueId) -> bool:
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def insert_one(self, user: UserIn) -> UserOut:
        pass

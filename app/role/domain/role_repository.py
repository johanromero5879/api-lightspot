from abc import ABC, abstractmethod

from app.common.domain import ValueId
from app.role.domain import RoleOut, BaseRole


class RoleRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[RoleOut]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> RoleOut | None:
        pass

    @abstractmethod
    def insert_many(self, roles: list[BaseRole]):
        pass

    @abstractmethod
    def replace_permissions(self, id: ValueId, permissions: list[str]):
        pass

from abc import ABC, abstractmethod

from app.common.domain import ValueId
from app.auth.domain import AuthOut


class AuthRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> AuthOut | None:
        pass

    @abstractmethod
    def find_by_id(self, user_id: ValueId) -> AuthOut | None:
        pass

    @abstractmethod
    def set_password(self, user_id: ValueId, password: str) -> bool:
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

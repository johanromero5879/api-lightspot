from abc import ABC, abstractmethod

from app.auth.domain import AuthOut


class AuthRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> AuthOut | None:
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

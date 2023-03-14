from app.role.domain import RoleRepository, RoleOut
from app.role.application import RoleNotFound


class FindRole:
    def __init__(self, role_repository: RoleRepository):
        self.__role_repository = role_repository

    def __call__(self, name: str) -> RoleOut:
        role = self.__role_repository.find_by_name(name)

        if not role:
            raise RoleNotFound(name)

        return role

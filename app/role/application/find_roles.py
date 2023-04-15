from app.role.domain import RoleRepository, RoleOut


class FindRoles:
    def __init__(self, role_repository: RoleRepository):
        self.__role_repository = role_repository

    def __call__(self) -> list[RoleOut]:
        roles = self.__role_repository.find_all()
        return roles

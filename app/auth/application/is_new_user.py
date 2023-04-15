from app.common.domain import ValueId
from app.auth.domain import AuthRepository
from app.user.application import UserNotFoundError


class IsNewUser:
    def __init__(self, auth_repository: AuthRepository):
        self.__auth_repository = auth_repository

    def __call__(self, user_id: ValueId) -> bool:
        user_found = self.__auth_repository.find_by_id(user_id)

        if not user_found:
            raise UserNotFoundError()

        return not user_found.password

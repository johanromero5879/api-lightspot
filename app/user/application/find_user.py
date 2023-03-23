from app.common.domain import ValueId
from app.user.domain import UserRepository, UserOut
from app.user.application import UserNotFoundError


class FindUser:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def __call__(self, id: ValueId, has_role: bool = False) -> UserOut:
        user = self.__user_repository.find_by_id(id, has_role)

        if not user:
            raise UserNotFoundError()

        return user

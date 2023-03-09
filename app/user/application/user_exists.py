from app.common.domain import ValueId
from app.user.domain import UserRepository


class UserExists:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def __call__(self, id: ValueId) -> bool:
        exists = self.__user_repository.exists_by_id(id)
        return exists

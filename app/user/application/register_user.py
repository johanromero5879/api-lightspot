from app.common.domain import ValueId
from app.user.domain import UserRepository, UserIn
from app.user.application import EmailFoundError


class RegisterUser:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    async def __call__(self, user: UserIn) -> ValueId:
        user.email = user.email.strip()
        user_found = self.__user_repository.exists_by_email(user.email)

        if user_found:
            raise EmailFoundError()

        user_id = self.__user_repository.insert_one(user)

        return user_id

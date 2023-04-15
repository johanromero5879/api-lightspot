from app.common.domain import ValueId
from app.common.application import BcryptAdapter
from app.auth.domain import AuthRepository


class RegisterPassword:
    def __init__(self, auth_repository: AuthRepository, bcrypt: BcryptAdapter):
        self.__auth_repository = auth_repository
        self.__bcrypt = bcrypt

    def __call__(self, user_id: ValueId, password: str) -> bool:
        password = self.__bcrypt.hash(password)
        return self.__auth_repository.set_password(user_id, password)

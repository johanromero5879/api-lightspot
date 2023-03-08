from app.common.domain import ValueId
from app.common.application import BcryptAdapter
from app.auth.domain import AuthRepository, CredentialsError


class AuthenticateUser:

    def __init__(self, auth_repository: AuthRepository, bcrypt: BcryptAdapter):
        self.__auth_repository = auth_repository
        self.__bcrypt = bcrypt

    def __call__(self, email: str, password: str) -> ValueId:
        user_found = self.__auth_repository.find_by_email(email)

        if not user_found or not self.__bcrypt.compare(password, user_found.password):
            raise CredentialsError()

        return user_found.id

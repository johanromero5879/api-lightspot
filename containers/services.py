from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, DependenciesContainer, Configuration, Factory

from app.common.application import BcryptAdapter
from app.common.infrastructure import MongoTransaction, JwtAdapter
from app.auth.application import AuthenticateUser


class Services(DeclarativeContainer):

    config = Configuration(strict=True)

    gateways = DependenciesContainer()
    repositories = DependenciesContainer()

    jwt = Singleton(JwtAdapter, secret_key=config.jwt_secret)
    bcrypt = Singleton(BcryptAdapter)
    transaction = Factory(MongoTransaction, client=gateways.database_client)

    authenticate_user = Singleton(
        AuthenticateUser,
        auth_repository=repositories.auth,
        bcrypt=bcrypt
    )

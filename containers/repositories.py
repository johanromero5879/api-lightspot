from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, DependenciesContainer

from app.auth.infrastructure import MongoAuthRepository
from app.role.infrastructure import MongoRoleRepository
from app.user.infrastructure import MongoUserRepository
from app.flash.infrastructure import MongoFlashRepository


class Repositories(DeclarativeContainer):

    gateways = DependenciesContainer()

    auth = Singleton(MongoAuthRepository, client=gateways.database_client)
    role = Singleton(MongoRoleRepository, client=gateways.database_client)
    user = Singleton(MongoUserRepository, client=gateways.database_client)
    flash = Singleton(MongoFlashRepository, client=gateways.database_client)

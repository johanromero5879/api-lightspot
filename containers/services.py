from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, DependenciesContainer, Configuration, Factory

from app.common.application import BcryptAdapter
from app.common.infrastructure import MongoTransaction, JwtAdapter

from app.role.application import FindRole

from app.auth.application import AuthenticateUser
from app.auth.infrastructure import GetUserPayload

from app.user.application import UserExists, FindUser

from app.flash.application import GetRawFlashes, GetFlashesRecord, InsertFlashes, FindFlashesBy, \
    GetInsights, FindFlashesByUser, RemoveFlashesLastDay
from app.flash.infrastructure import NominatimReverseGeocode


class Services(DeclarativeContainer):

    config = Configuration(strict=True)

    gateways = DependenciesContainer()
    repositories = DependenciesContainer()

    jwt = Singleton(JwtAdapter, secret_key=config.jwt_secret)
    bcrypt = Singleton(BcryptAdapter)
    transaction = Factory(MongoTransaction, client=gateways.database_client)

    # auth
    authenticate_user = Singleton(
        AuthenticateUser,
        auth_repository=repositories.auth,
        bcrypt=bcrypt
    )

    get_user_payload = Singleton(
        GetUserPayload,
        jwt=jwt
    )

    find_role = Singleton(
        FindRole,
        role_repository=repositories.role
    )

    # user
    user_exists = Singleton(
        UserExists,
        user_repository=repositories.user
    )

    find_user = Singleton(
        FindUser,
        user_repository=repositories.user
    )

    # flash
    reverse_geocode = Singleton(
        NominatimReverseGeocode,
        api_uri=config.geolocator_api
    )

    get_raw_flashes = Singleton(GetRawFlashes)

    get_flashes_record = Singleton(
        GetFlashesRecord,
        reverse_geocode=reverse_geocode
    )

    insert_flashes = Singleton(
        InsertFlashes,
        flash_repository=repositories.flash
    )

    find_flashes_by = Singleton(
        FindFlashesBy,
        flash_repository=repositories.flash
    )

    find_flashes_by_user = Singleton(
        FindFlashesByUser,
        flash_repository=repositories.flash
    )

    get_insights = Singleton(
        GetInsights,
        flash_repository=repositories.flash
    )

    remove_flashes_last_day = Singleton(
        RemoveFlashesLastDay,
        flash_repository=repositories.flash
    )

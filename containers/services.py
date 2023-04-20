from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, DependenciesContainer, Configuration, Factory

from app.common.application import BcryptAdapter
from app.common.infrastructure import MongoTransaction, JwtAdapter, SendEmail

from app.role.application import FindRole, FindRoles

from app.auth.application import AuthenticateUser, IsNewUser, RegisterPassword
from app.auth.infrastructure import GetUserPayload

from app.user.application import UserExists, FindUser, RegisterUser, SendEmailToNewUser, FindUsers

from app.flash.application import GetRawFlashes, GetFlashesRecord, InsertFlashes, FindFlashesBy, \
    GetInsights, FindFlashesByUser, RemoveFlashesLastDay, ExistsFile
from app.flash.infrastructure import NominatimReverseGeocode


class Services(DeclarativeContainer):

    config = Configuration(strict=True)

    gateways = DependenciesContainer()
    repositories = DependenciesContainer()

    jwt = Singleton(JwtAdapter, secret_key=config.jwt_secret)
    bcrypt = Singleton(BcryptAdapter)
    transaction = Factory(MongoTransaction, client=gateways.database_client)

    # common
    send_email = Singleton(
        SendEmail,
        server=config.smtp.server,
        username=config.smtp.username,
        password=config.smtp.password
    )

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

    is_new_user = Singleton(
        IsNewUser,
        auth_repository=repositories.auth
    )

    register_password = Singleton(
        RegisterPassword,
        auth_repository=repositories.auth,
        bcrypt=bcrypt
    )

    find_roles = Singleton(
        FindRoles,
        role_repository=repositories.role
    )

    find_role = Singleton(
        FindRole,
        role_repository=repositories.role
    )

    exists_by_name = Singleton(
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

    find_users = Singleton(
        FindUsers,
        user_repository=repositories.user
    )

    register_user = Singleton(
        RegisterUser,
        user_repository=repositories.user
    )

    send_email_to_new_user = Singleton(
        SendEmailToNewUser,
        send_email=send_email,
        client_url=config.client.url,
        jwt=jwt
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

    exists_flashes_file = Singleton(
        ExistsFile,
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

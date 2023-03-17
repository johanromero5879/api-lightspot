from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from dependency_injector.wiring import Provide, inject


from app.user.application import UserNotFoundError, FindUser
from app.role.application import FindRole, RoleNotFound
from app.auth.infrastructure import AuthTokenError, GetUserPayload, AuthorizationError

from config import WHITELIST

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/token")


@inject
async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2),
    get_user_payload: GetUserPayload = Depends(Provide["services.get_user_payload"]),
    find_user: FindUser = Depends(Provide["services.find_user"]),

):
    try:
        payload = get_user_payload(token)
        user = find_user(payload.user_id)

        if security_scopes.scopes:
            await check_permissions(
                role_name=user.role,
                scopes=security_scopes.scopes
            )

        return user
    except UserNotFoundError:
        raise AuthTokenError("invalid refresh token")


@inject
async def check_permissions(
    role_name: str,
    scopes: list[str],
    find_role: FindRole = Depends(Provide["services.find_role"])
):
    try:
        role = find_role(role_name)

        for scope in scopes:
            if scope not in role.permissions:
                raise AuthorizationError("not enough permissions")

    except RoleNotFound as error:
        raise AuthorizationError(detail=str(error))


async def verify_device_address(request: Request):
    if request.headers.get("x-forwarded-for"):
        address = request.headers.get("x-forwarded-for")
    else:
        address = request.client.host

    if address not in WHITELIST:
        raise AuthorizationError("this device is not allowed")

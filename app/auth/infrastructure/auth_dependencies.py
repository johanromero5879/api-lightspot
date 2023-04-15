from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from dependency_injector.wiring import Provide, inject

from app.common.domain import ValueId
from app.user.domain import UserOut
from app.user.application import UserNotFoundError, FindUser
from app.role.application import RoleNotFound
from app.auth.application import IsNewUser
from app.auth.infrastructure import AuthTokenError, GetUserPayload, AuthorizationError, TokenData

from config import WHITELIST

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/token")


@inject
def get_payload(
    token: str = Depends(oauth2),
    get_user_payload: GetUserPayload = Depends(Provide["services.get_user_payload"])
) -> TokenData:
    payload = get_user_payload(token)
    return payload


@inject
def get_new_user_id(
    payload: TokenData = Depends(get_payload),
    is_new_user: IsNewUser = Depends(Provide["services.is_new_user"])
) -> ValueId | None:
    try:
        if is_new_user(payload.user_id):
            return payload.user_id

    except UserNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )


@inject
async def get_current_user(
    security_scopes: SecurityScopes,
    payload: TokenData = Depends(get_payload),
    find_user: FindUser = Depends(Provide["services.find_user"])
):
    try:
        user = find_user(
            id=payload.user_id,
            has_role=True
        )

        if security_scopes.scopes:
            check_permissions(user, security_scopes.scopes)

        return user
    except UserNotFoundError:
        raise AuthTokenError("invalid refresh token")
    except RoleNotFound as error:
        raise AuthorizationError(detail=str(error))


def check_permissions(
    user: UserOut,
    scopes: list[str]
):
    for scope in scopes:
        if scope not in user.role.permissions:
            raise AuthorizationError("not enough permissions")


async def verify_device_address(request: Request):
    if request.headers.get("x-forwarded-for"):
        address = request.headers.get("x-forwarded-for")
    else:
        address = request.client.host

    if address not in WHITELIST:
        raise AuthorizationError("this device is not allowed")

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import Provide, inject


from app.user.application import UserNotFoundError, FindUser
from app.auth.infrastructure import AuthTokenError, GetUserPayload

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/token")


@inject
async def get_current_user(
    token: str = Depends(oauth2),
    get_user_payload: GetUserPayload = Depends(Provide["services.get_user_payload"]),
    find_user: FindUser = Depends(Provide["services.find_user"]),
):
    try:
        payload = get_user_payload(token)
        user = find_user(payload.user_id)

        return user
    except UserNotFoundError:
        raise AuthTokenError("invalid refresh token")

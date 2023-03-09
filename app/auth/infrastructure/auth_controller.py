from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from dependency_injector.wiring import inject, Provide

from app.common.domain import ValueId
from app.common.infrastructure import JwtAdapter

from app.auth.application import AuthenticateUser, CredentialsError
from app.auth.domain import AuthIn
from app.auth.infrastructure import AuthTokenError, Token, GetUserPayload

from app.user.application import UserExists

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post(
    path="/token",
    response_model=Token
)
@inject
async def login(
    response: Response,
    auth: AuthIn,
    authenticate_user: AuthenticateUser = Depends(Provide["services.authenticate_user"])
):
    """
    :param response: This is used to generate the HTTP response that will be sent back to the client.
    :param auth: Model representing the authentication information in the request body.
    :param authenticate_user: A dependency that is used to authenticate the user based on provided email and password.
    :return: A Token object that represents the access token.
    """
    try:
        user_id = authenticate_user(auth.email, auth.password)

        access_token, refresh_token = generate_tokens(user_id)

        return generate_token_response(response, access_token, refresh_token)
    except CredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )


@router.post(
    path="/token/refresh",
    response_model=Token
)
@inject
def refresh(
    response: Response,
    refresh_token: str = Cookie(None),
    user_exists: UserExists = Depends(Provide["services.user_exists"]),
    get_user_payload: GetUserPayload = Depends(Provide["services.get_user_payload"])
):
    if not refresh_token:
        raise AuthTokenError("missing refresh token")

    # Get user_id from the refresh_token
    payload = get_user_payload(refresh_token)

    if not user_exists(payload.user_id):
        raise AuthTokenError("invalid refresh token")

    # Generate new tokens
    access_token, refresh_token = generate_tokens(payload.user_id)

    return generate_token_response(response, access_token, refresh_token)


@inject
def generate_tokens(
    user_id: ValueId,
    jwt: JwtAdapter = Depends(Provide["services.jwt"])
) -> tuple[str, str]:
    """
    Generates and returns two tokens, an access token and a refresh token, for a given user ID.
    :param user_id: It represents the unique identifier of the user for which the tokens are generated.
    :param jwt: It represents a JWT (JSON Web Token) adapter that is used to create the tokens.
    :return: A tuple of two strings representing the access token and refresh token, respectively.
    """
    identifier = f"user_id:{user_id}"
    access_token = jwt.create_access_token(identifier)
    refresh_token = jwt.create_refresh_token(identifier)

    return access_token, refresh_token


def generate_token_response(response: Response, access_token: str, refresh_token: str) -> Token:
    """
    :param response: This is used to generate the HTTP response that will be sent back to the client.
    :param access_token: A string representing a JWT access token
    :param refresh_token: A string representing a JWT refresh token
    :return: A Token object that represents the generated access token.
    """
    refresh_token_expire_seconds = JwtAdapter.REFRESH_TOKEN_EXPIRE_MINUTES * 60

    # This code sets an HTTP-only cookie named refresh_token in the HTTP response.
    # The httponly flag is set to True, which prevents the cookie from being accessed by JavaScript.
    # The path parameter is set to /auth/token/refresh, which restricts the cookie
    # to only be sent to requests made to this path.
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=refresh_token_expire_seconds,
        path="/auth/token/refresh"
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )

from fastapi import APIRouter, Depends, HTTPException, status, Response

from dependency_injector.wiring import inject, Provide

from app.common.infrastructure import JwtAdapter

from app.auth.application import AuthenticateUser
from app.auth.domain import AuthIn, CredentialsError
from app.auth.infrastructure import Token

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
    authenticate_user: AuthenticateUser = Depends(Provide["services.authenticate_user"]),
    jwt: JwtAdapter = Depends(Provide["services.jwt"])
):
    try:
        user_id = authenticate_user(auth.email, auth.password)

        # Generate tokens
        identifier = f"user_id:{user_id}"
        access_token = jwt.create_access_token(identifier)
        refresh_token = jwt.create_refresh_token(identifier)

        return generate_token_response(response, access_token, refresh_token)
    except CredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )


def generate_token_response(response: Response, access_token: str, refresh_token: str) -> Token:
    refresh_token_expire_seconds = JwtAdapter.REFRESH_TOKEN_EXPIRE_MINUTES * 60

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=refresh_token_expire_seconds,
        path="/auth/token/refresh"  # Cookie only be sent to this path
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )

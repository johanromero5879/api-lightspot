from app.common.infrastructure import JwtAdapter

from app.auth.infrastructure import TokenData, AuthTokenError


class GetUserPayload:
    def __init__(self, jwt: JwtAdapter):
        self.__jwt = jwt

    def __call__(self, token: str) -> TokenData:
        try:
            token_decoded = self.__jwt.decrypt(token)
            user_id = token_decoded.sub.replace("user_id:", "")

            payload = TokenData(
                user_id=user_id
            )
        except Exception:
            raise AuthTokenError("invalid token or expired")

        return payload

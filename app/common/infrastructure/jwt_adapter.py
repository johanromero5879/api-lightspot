from datetime import datetime, timedelta

from authlib.jose import jwt
from pydantic import BaseModel


class JwtToken(BaseModel):
    sub: str
    exp: datetime


class JwtAdapter:
    __secret_key: str

    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    def __init__(self, secret_key: str):
        self.__secret_key = secret_key

    def create_access_token(self, identifier: str) -> str:
        return self.encrypt(identifier, self.ACCESS_TOKEN_EXPIRE_MINUTES)

    def create_refresh_token(self, identifier: str) -> str:
        return self.encrypt(identifier, self.REFRESH_TOKEN_EXPIRE_MINUTES)

    def encrypt(self, identifier: str, expires_minutes: int) -> str:
        """
        :param identifier: A string that identifies certain resource
        :param expires_minutes: Time expiration given in minutes
        :return: JWT Token
        """
        header = {"alg": self.ALGORITHM}

        payload = {
            "sub": identifier,
            "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)
        }

        return jwt.encode(header, payload, self.__secret_key).decode("utf-8")

    def decrypt(self, token: str) -> JwtToken:
        decoded_jwt = jwt.decode(token, self.__secret_key)
        return JwtToken(**decoded_jwt)

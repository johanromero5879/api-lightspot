from os import getenv

ALLOWED_ORIGINS = [
    getenv("CLIENT_URL")
]

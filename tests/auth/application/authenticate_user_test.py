from app.auth.domain import CredentialsError
from app.auth.application import AuthenticateUser


def test_authenticate_correct_credentials(container):
    authenticate_user: AuthenticateUser = container.services.authenticate_user()

    credentials = [
        {"email": "john.titor@cern.ch", "password": "Super.secret123"},
        {"email": "rachell@outlook.com", "password": "Super.secret123"}
    ]

    for credential in credentials:
        try:
            authenticate_user(credential["email"], credential["password"])
            assert True
        except CredentialsError:
            assert False


def test_authenticate_incorrect_credentials(container):
    authenticate_user: AuthenticateUser = container.services.authenticate_user()

    credentials = [
        {"email": "daniela_chaparro@gmail.com", "password": "cl4ss1c_"},
        {"email": "sara.claire@gmail.com", "password": "Super.secret123"}
    ]

    for credential in credentials:
        try:
            authenticate_user(credential["email"], credential["password"])
            assert False
        except CredentialsError:
            assert True

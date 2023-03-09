class CredentialsError(Exception):
    def __init__(self):
        message = "could not validate credentials"
        super().__init__(message)

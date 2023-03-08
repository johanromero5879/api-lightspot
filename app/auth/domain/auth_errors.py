class CredentialsError(Exception):
    def __init__(self):
        message = "Could not validate credentials"
        super().__init__(message)

class UserNotFoundError(Exception):
    def __init__(self):
        message = "user not found"
        super().__init__(message)

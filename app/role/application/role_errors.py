class RoleNotFound(Exception):
    def __init__(self, name: str):
        message = f"role {name} not found"
        super().__init__(message)

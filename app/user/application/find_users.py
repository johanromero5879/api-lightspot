from app.user.domain import UserRepository, UserList


class FindUsers:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def __call__(self, limit: int, page: int, has_role: bool = False) -> UserList:
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        if page <= 0:
            raise ValueError("page must be greater than zero")

        skip = (page - 1) * limit
        users = self.__user_repository.find_all(limit, skip, has_role)
        return users

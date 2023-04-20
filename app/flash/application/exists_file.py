from app.flash.domain import FlashRepository


class ExistsFile:
    def __init__(self, flash_repository: FlashRepository):
        self.__flash_repository = flash_repository

    async def __call__(self, filename: str) -> bool:
        return await self.__flash_repository.exists_file(filename)

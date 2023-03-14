from app.flash.domain import FlashIn, FlashRepository


class InsertFlashes:
    def __init__(self, flash_repository: FlashRepository):
        self.__flash_repository = flash_repository

    async def __call__(self, flashes: list[FlashIn]):
        await self.__flash_repository.insert_many(flashes)

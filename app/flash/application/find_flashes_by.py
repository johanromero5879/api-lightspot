from app.flash.domain import FlashRepository, FlashQuery


class FindFlashesBy:
    def __init__(self, flash_repository: FlashRepository):
        self.__flash_repository = flash_repository

    async def __call__(self, query: FlashQuery, utc_offset: str):
        if query.date_range.start_date > query.date_range.end_date:
            raise ValueError("Start date must be before end date")

        flashes = await self.__flash_repository.find_by(query, utc_offset)

        return flashes

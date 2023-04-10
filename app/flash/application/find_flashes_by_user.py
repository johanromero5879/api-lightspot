from datetime import datetime

from app.common.domain import ValueId
from app.common.application import subtract_time
from app.flash.domain import FlashRepository, FlashOut


class FindFlashesByUser:
    def __init__(self, flash_repository: FlashRepository):
        self.__flash_repository = flash_repository

    async def __call__(self, user_id: ValueId, period: str) -> list[FlashOut]:
        today = datetime.utcnow()
        start_date = subtract_time(today, period)

        flashes = await self.__flash_repository.find_by_user(user_id, start_date)

        return flashes


from datetime import datetime

from app.common.domain import ValueId
from app.common.application import subtract_time
from app.flash.domain import FlashRepository


class RemoveFlashesLastDay:
    def __init__(self, flash_repository: FlashRepository):
        self.__flash_repository = flash_repository

    async def __call__(self, user_id: ValueId) -> bool:
        today = datetime.utcnow()
        start_date = subtract_time(today, "1 days")

        return await self.__flash_repository.delete_many_by_user(user_id, start_date)

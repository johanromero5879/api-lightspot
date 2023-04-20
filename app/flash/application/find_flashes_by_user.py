from asyncio import create_task, gather
from datetime import datetime

from app.common.domain import ValueId
from app.common.application import subtract_time
from app.flash.domain import FlashRepository


class FindFlashesByUser:
    def __init__(self, flash_repository: FlashRepository):
        self.__flash_repository = flash_repository

    async def __call__(self, user_id: ValueId, period: str):
        today = datetime.utcnow()
        start_date = subtract_time(today, period)

        files_task = create_task(self.__flash_repository.find_files_by(user_id, start_date))
        flashes_task = create_task(self.__flash_repository.find_by_user(user_id, start_date))

        files, flashes = await gather(files_task, flashes_task)

        return {
            "files": files,
            "flashes": flashes
        }

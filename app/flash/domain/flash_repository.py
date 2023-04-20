from abc import ABC, abstractmethod
from datetime import datetime

from app.common.domain import ValueId
from app.flash.domain import FlashIn, FlashQuery, FlashOut


class FlashRepository(ABC):
    @abstractmethod
    async def insert_many(self, flashes: list[FlashIn]):
        pass

    @abstractmethod
    async def find_by(self, query: FlashQuery, utc_offset: str) -> list[FlashOut]:
        pass

    @abstractmethod
    async def exists_file(self, file: str) -> bool:
        pass

    @abstractmethod
    async def find_by_user(self, user_id: ValueId, start_date: datetime) -> list[FlashOut]:
        pass

    @abstractmethod
    async def delete_many_by_user(self, user_id: ValueId, start_date: datetime, file: str | None = None) -> bool:
        pass

    @abstractmethod
    async def find_files_by(self, user_id: ValueId, start_date: datetime) -> list[str]:
        pass

    @abstractmethod
    async def count_yearly(self, query: FlashQuery, utc_offset: str):
        pass

    @abstractmethod
    async def count_hourly(self, query: FlashQuery, utc_offset: str):
        pass

    @abstractmethod
    async def count_by_cities(self, query: FlashQuery):
        pass

from abc import ABC, abstractmethod

from app.flash.domain import FlashIn, FlashQuery, FlashOut


class FlashRepository(ABC):
    @abstractmethod
    async def insert_many(self, flashes: list[FlashIn]):
        pass

    @abstractmethod
    async def find_by(self, query: FlashQuery, utc_offset: str) -> list[FlashOut]:
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

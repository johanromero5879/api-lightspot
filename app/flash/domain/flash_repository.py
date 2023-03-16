from abc import ABC, abstractmethod

from app.flash.domain import FlashIn, FlashQuery, FlashOut


class FlashRepository(ABC):
    @abstractmethod
    async def insert_many(self, flashes: list[FlashIn]):
        pass

    @abstractmethod
    async def find_by(self, query: FlashQuery) -> list[FlashOut]:
        pass

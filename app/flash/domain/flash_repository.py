from abc import ABC, abstractmethod

from app.flash.domain import FlashIn


class FlashRepository(ABC):
    @abstractmethod
    async def insert_many(self, flashes: list[FlashIn]):
        pass

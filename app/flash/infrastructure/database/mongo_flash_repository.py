from pymongo import MongoClient

from app.common.infrastructure import MongoAdapter
from app.flash.domain import FlashRepository, FlashIn


class MongoFlashRepository(MongoAdapter, FlashRepository):
    def __init__(self, client: MongoClient | None = None):
        super().__init__("flashes", client)

    async def insert_many(self, flashes: list[FlashIn]):
        self.collection.insert_many(
            [flash.dict(exclude_none=True) for flash in flashes]
        )

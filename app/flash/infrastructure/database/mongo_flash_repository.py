from datetime import datetime

from pymongo import MongoClient, DESCENDING

from app.common.infrastructure import MongoAdapter
from app.flash.domain import FlashRepository, FlashIn, FlashQuery, FlashOut


class MongoFlashRepository(MongoAdapter, FlashRepository):
    def __init__(self, client: MongoClient | None = None):
        super().__init__("flashes", client)

    async def insert_many(self, flashes: list[FlashIn]):
        self.collection.insert_many(
            [flash.dict(exclude_none=True) for flash in flashes]
        )

    async def find_by(self, query: FlashQuery) -> list[FlashOut]:
        formatted_query = self.format_query(query)
        flashes = self.collection\
            .find(
                filter=formatted_query,
                projection={"created_at": 0, "user": 0}
            )\
            .sort("occurrence_date", DESCENDING).limit(50_000)

        return [FlashOut(**flash) for flash in flashes]

    def format_query(self, query: FlashQuery) -> dict:
        formatted_query = dict()
        date_range = query.date_range
        location = query.location

        formatted_query["occurrence_date"] = {
            "$gte": datetime.combine(date_range.start_date, datetime.min.time()),
            "$lte": datetime.combine(date_range.end_date, datetime.max.time())
        }

        if location.country:
            formatted_query["location.country"] = location.country

        if location.state:
            formatted_query["location.state"] = location.state

        if location.city:
            formatted_query["location.city"] = location.city

        return formatted_query

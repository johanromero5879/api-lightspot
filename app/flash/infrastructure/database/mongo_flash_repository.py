from datetime import datetime

from bson import ObjectId
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

    async def exists_file(self, file: str) -> bool:
        flashes = self.collection.find_one(
            filter={"file": file},
            projection={"_id": 1}
        )

        return bool(flashes)

    async def find_files_by(self, user_id: ObjectId, start_date: datetime) -> list[str]:
        files = self.collection.aggregate([
            {"$match": {"user": user_id, "created_at": {"$gte": start_date}}},
            {"$sort": {"created_at": DESCENDING}},
            {"$group": {"_id": "$file"}}
        ])

        return [file["_id"] for file in files]

    async def find_by_user(self, user_id: ObjectId, start_date: datetime) -> list[FlashOut]:
        flashes = self.collection.find(
            filter={"user": user_id, "created_at": {"$gte": start_date}},
            projection={"user": 0}
        ).sort("occurrence_date", DESCENDING)

        return [FlashOut(**flash) for flash in flashes]

    async def find_by(self, query: FlashQuery, utc_offset: str) -> list[FlashOut]:
        formatted_query = self.format_query(query)
        projection = {
            "lat": 1,
            "lon": 1,
            "residual_fit_error": 1,
            "stations": 1,
            "location": 1,
            "occurrence_date": {
                "$dateToString": {
                    "format": "%Y-%m-%d %H:%M:%S.%L",
                    "timezone": utc_offset,
                    "date": "$occurrence_date"
                }
            }
        }

        flashes = self.collection\
            .find(
                filter=formatted_query,
                projection=projection
            )\
            .sort("occurrence_date", DESCENDING)

        return [FlashOut(**flash) for flash in flashes]

    async def delete_many_by_user(
        self,
        user_id: ObjectId,
        start_date: datetime,
        file: str | None = None
    ) -> bool:
        filter = {"user": user_id, "created_at": {"$gte": start_date}}

        if file:
            filter["file"] = file

        result = self.collection.delete_many(filter=filter)

        return result.deleted_count > 0

    async def count_yearly(self, query: FlashQuery, utc_offset: str):
        formatted_query = self.format_query(query)

        results = self.collection.aggregate([
            {"$match": formatted_query},
            {"$group": {
                "_id": {
                    "year": {"$year": {"date": "$occurrence_date", "timezone": utc_offset}},
                    "month": {"$month": {"date": "$occurrence_date", "timezone": utc_offset}}
                },
                "total": {"$sum": 1}
            }},
            {"$project": {
                "_id": 0,
                "year": "$_id.year",
                "month": "$_id.month",
                "total": "$total"
            }},
            {"$sort": {"year": DESCENDING, "month": DESCENDING}}
        ])

        return [result for result in results]

    async def count_hourly(self, query: FlashQuery, utc_offset: str):
        formatted_query = self.format_query(query)

        results = self.collection.aggregate([
            {"$match": formatted_query},
            {"$group": {
                "_id": {
                    "$hour": {"date": "$occurrence_date", "timezone": utc_offset},
                },
                "total": {"$sum": 1}
            }},
            {"$project": {
                "_id": 0,
                "hour": "$_id",
                "total": "$total"
            }},
            {"$sort": {"total": DESCENDING}}
        ])

        return [result for result in results]

    async def count_by_cities(self, query: FlashQuery):
        formatted_query = self.format_query(query)

        results = self.collection.aggregate([
            {"$match": formatted_query},
            {"$group": {
                "_id": "$location.city", "total": {"$sum": 1}
            }},
            {"$project": {
                "_id": 0,
                "city": "$_id",
                "total": "$total"}},
            {"$sort": {"total": DESCENDING}},
        ])

        return [result for result in results]

    def format_query(self, query: FlashQuery) -> dict:
        formatted_query = dict()
        date_range = query.date_range
        location = query.location

        formatted_query["occurrence_date"] = {
            "$gte": date_range.start_date,
            "$lte": date_range.end_date
        }

        if location.country:
            formatted_query["location.country"] = location.country

        if location.state:
            formatted_query["location.state"] = location.state

        if location.city:
            formatted_query["location.city"] = location.city

        return formatted_query

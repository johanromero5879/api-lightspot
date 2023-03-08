from abc import ABC

from pymongo import MongoClient


class MongoAdapter(ABC):
    __client: MongoClient
    __collection_name: str

    @property
    def collection(self):
        return self.__client.get_database().get_collection(self.__collection_name)

    def __init__(self, collection_name: str, client: MongoClient | None = None):
        self.__client = client or MongoClient()
        self.__collection_name = collection_name

    def disconnect(self):
        self.__client.close()

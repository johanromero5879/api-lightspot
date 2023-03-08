from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton
from pymongo import MongoClient


class Gateways(DeclarativeContainer):

    config = Configuration(strict=True)

    database_client = Singleton(MongoClient, config.database.mongo)

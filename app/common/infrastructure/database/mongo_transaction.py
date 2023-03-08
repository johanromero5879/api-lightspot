from pymongo import MongoClient
from pymongo.client_session import ClientSession

from app.common.application import Transaction


class MongoTransaction(Transaction):
    __client: MongoClient
    __session: ClientSession

    def __init__(self, client: MongoClient):
        self.__client = client

    def get_session(self):
        return self.__session

    def start(self):
        self.__session = self.__client.start_session()
        self.__session.start_transaction()

    def commit(self):
        if self.__session:
            self.__session.commit_transaction()
            self.__session.end_session()

    def rollback(self):
        if self.__session:
            self.__session.abort_transaction()
            self.__session.end_session()

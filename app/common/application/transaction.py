from abc import ABC, abstractmethod


class Transaction(ABC):
    """
    Represents a transaction when many database operations are required for a single action
    and all the success operations makes a completed action,
    otherwise these operations must not save changes on database
    """

    @abstractmethod
    def get_session(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

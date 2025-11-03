from abc import ABC, abstractmethod

from src.models import Transaction


class StorageServiceException(Exception):
    pass


class StorageService(ABC):
    @abstractmethod
    def store_statement(self, statement_bytes: bytes, bank_name: str, year: int, month: int) -> None:
        pass

    @abstractmethod
    def get_statement_for_bank_on_date(self, bank_name: str, year: int, month: int) -> str:
        pass

    @abstractmethod
    def store_transactions(self, transactions: list[Transaction], bank_name: str, year: int, month: int) -> None:
        pass

    @abstractmethod
    def get_transactions_for_bank_for_date(self, bank_name: str, year: int, month: int) -> list[Transaction]:
        pass

    @abstractmethod
    def get_all_transactions_for_bank(self, bank_name: str) -> list[Transaction]:
        pass

    @abstractmethod
    def get_all_transactions_for_date(self, year: int, month: int) -> list[Transaction]:
        pass

    @abstractmethod
    def get_all_transactions_for_bank_for_year(self, bank_name: str, year: int) -> list[Transaction]:
        pass

    @abstractmethod
    def get_all_transactions_for_year(self, year: int) -> list[Transaction]:
        pass

    @abstractmethod
    def get_all_transactions(self) -> list[Transaction]:
        pass

from abc import ABC, abstractmethod

from src.models import ParsedTransactions


class StorageService(ABC):
    @abstractmethod
    def store_statement(self, statement_bytes: bytes, bank_name: str, year: int, month: int) -> None:
        pass

    @abstractmethod
    def get_statement(self, bank_name: str, year: int, month: int) -> str:
        pass

    @abstractmethod
    def store_parsed_transactions(
        self, parsed_transactions: ParsedTransactions, bank_name: str, year: int, month: int
    ) -> None:
        pass

    @abstractmethod
    def get_parsed_transactions(self, bank_name: str, year: int, month: int) -> ParsedTransactions:
        pass

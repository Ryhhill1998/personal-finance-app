from src.models import ParsedTransactions


class StorageService:
    def __init__(self):
        pass

    def store_statement(self, statement_bytes: bytes, storage_path: str) -> None:
        pass

    def get_statement(self) -> str:
        pass

    def store_parsed_transactions(self) -> None:
        pass

    def get_parsed_transactions(self) -> ParsedTransactions:
        pass

import json
from pathlib import Path

from src.models import ParsedTransactions
from src.services.storage.storage_service import StorageService


class LocalStorageService(StorageService):
    def __init__(self, storage_dir_path: Path):
        self.storage_dir_path = storage_dir_path

    def store_statement(self, statement_bytes: bytes, bank_name: str, year: int, month: int) -> None:
        dir_path = self.storage_dir_path / bank_name / "raw"
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / f"Statement_{year}_{month}.pdf"
        file_path.write_bytes(statement_bytes)

    def get_statement(self, bank_name: str, year: int, month: int) -> str:
        dir_path = self.storage_dir_path / bank_name / "raw"
        file_path = dir_path / f"Statement_{year}_{month}.pdf"
        return file_path.read_text()

    def store_parsed_transactions(
        self, parsed_transactions: ParsedTransactions, bank_name: str, year: int, month: int
    ) -> None:
        dir_path = self.storage_dir_path / bank_name / "parsed"
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / f"Statement_{year}_{month}.json"

        with open(file_path, "w") as parsed_file:
            json.dump(parsed_transactions.model_dump_json(), parsed_file)

    def get_parsed_transactions(self, bank_name: str, year: int, month: int) -> ParsedTransactions:
        pass

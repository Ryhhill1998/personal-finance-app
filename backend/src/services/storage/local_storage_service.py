import json
from pathlib import Path

from pydantic import ValidationError

from src.models import ParsedTransactions
from src.services.storage.storage_service import StorageService, StorageServiceException


class LocalStorageService(StorageService):
    def __init__(self, storage_dir_path: Path):
        self.storage_dir_path = storage_dir_path

    def store_statement(self, statement_bytes: bytes, bank_name: str, year: int, month: int) -> None:
        dir_path = self.storage_dir_path / bank_name / "raw"
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / f"Statement_{year}_{month:02}.pdf"
        file_path.write_bytes(statement_bytes)

    def get_statement_for_bank_on_date(self, bank_name: str, year: int, month: int) -> str:
        dir_path = self.storage_dir_path / bank_name / "raw"
        file_path = dir_path / f"Statement_{year}_{month:02}.pdf"

        try:
            return file_path.read_text()
        except FileNotFoundError:
            raise StorageServiceException(f"Could not find file at path: {file_path}")

    def store_parsed_transactions(
        self, parsed_transactions: ParsedTransactions, bank_name: str, year: int, month: int
    ) -> None:
        dir_path = self.storage_dir_path / bank_name / "parsed"
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / f"Statement_{year}_{month:02}.json"

        with open(file_path, "w") as parsed_file:
            parsed_file.write(parsed_transactions.model_dump_json())

    def get_parsed_transactions_for_bank_on_date(self, bank_name: str, year: int, month: int) -> ParsedTransactions:
        dir_path = self.storage_dir_path / bank_name / "parsed"
        file_path = dir_path / f"Statement_{year}_{month:02}.json"

        try:
            with open(file_path) as parsed_file:
                json_data = json.load(parsed_file)

            return ParsedTransactions(**json_data)
        except FileNotFoundError:
            raise StorageServiceException(f"Could not find file at path: {file_path}")
        except ValidationError:
            raise StorageServiceException(f"Failed to convert json data into ParsedTransactions object")

    def get_parsed_transactions_for_date(self, year: int, month: int) -> list[ParsedTransactions]:
        all_parsed_transactions: list[ParsedTransactions] = []

        for bank_dir in self.storage_dir_path.iterdir():
            bank_name = bank_dir.name
            parsed_transactions = self.get_parsed_transactions_for_bank_on_date(
                bank_name=bank_name, year=year, month=month
            )
            all_parsed_transactions.append(parsed_transactions)

        return all_parsed_transactions

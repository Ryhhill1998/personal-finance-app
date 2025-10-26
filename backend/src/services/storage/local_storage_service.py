import json
from pathlib import Path

from pydantic import ValidationError

from src.models import ParsedTransactions
from src.services.storage.storage_service import StorageService, StorageServiceException


class LocalStorageService(StorageService):
    def __init__(self, storage_dir_path: Path):
        self.storage_dir_path = storage_dir_path

    def store_statement(self, statement_bytes: bytes, bank_name: str, year: int, month: int) -> None:
        dir_path = self.storage_dir_path / bank_name / str(year) / f"{month:02}"
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / "statement.pdf"
        file_path.write_bytes(statement_bytes)

    def get_statement_for_bank_on_date(self, bank_name: str, year: int, month: int) -> str:
        file_path = self.storage_dir_path / bank_name / str(year) / f"{month:02}" / "statement.pdf"

        try:
            return file_path.read_text()
        except FileNotFoundError:
            raise StorageServiceException(f"Could not find file at path: {file_path}")

    def store_parsed_transactions(
        self, parsed_transactions: ParsedTransactions, bank_name: str, year: int, month: int
    ) -> None:
        dir_path = self.storage_dir_path / bank_name / str(year) / f"{month:02}"
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / "transactions.json"

        with open(file_path, "w") as parsed_file:
            parsed_file.write(parsed_transactions.model_dump_json())

    def get_parsed_transactions_for_bank_for_date(self, bank_name: str, year: int, month: int) -> ParsedTransactions:
        file_path = self.storage_dir_path / bank_name / str(year) / f"{month:02}" / "transactions.json"

        try:
            with open(file_path) as parsed_file:
                json_data = json.load(parsed_file)

            return ParsedTransactions(**json_data)
        except FileNotFoundError:
            raise StorageServiceException(f"Could not find file at path: {file_path}")
        except ValidationError:
            raise StorageServiceException(f"Failed to convert json data into ParsedTransactions object")

    def get_all_parsed_transactions_for_bank(self, bank_name: str) -> list[ParsedTransactions]:
        all_parsed_transactions_for_bank: list[ParsedTransactions] = []
        bank_dir_path = self.storage_dir_path / bank_name

        for year_dir_path in bank_dir_path.iterdir():
            year = year_dir_path.name

            for month_dir_path in (bank_dir_path / year).iterdir():
                month = month_dir_path.name

                parsed_transactions_for_bank_for_date = self.get_parsed_transactions_for_bank_for_date(
                    bank_name=bank_name, year=int(year), month=int(month)
                )
                all_parsed_transactions_for_bank.append(parsed_transactions_for_bank_for_date)

        return all_parsed_transactions_for_bank

    def get_all_parsed_transactions_for_date(self, year: int, month: int) -> list[ParsedTransactions]:
        all_parsed_transactions_for_date: list[ParsedTransactions] = []

        for bank_dir in self.storage_dir_path.iterdir():
            bank_name = bank_dir.name
            parsed_transactions_for_date = self.get_parsed_transactions_for_bank_for_date(
                bank_name=bank_name, year=year, month=month
            )
            all_parsed_transactions_for_date.append(parsed_transactions_for_date)

        return all_parsed_transactions_for_date

    def get_all_parsed_transactions(self, year: int, month: int) -> list[ParsedTransactions]:
        all_parsed_transactions: list[ParsedTransactions] = []

        for bank_dir in self.storage_dir_path.iterdir():
            bank_name = bank_dir.name

        return all_parsed_transactions

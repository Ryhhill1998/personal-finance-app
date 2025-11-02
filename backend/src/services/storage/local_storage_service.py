import json
from pathlib import Path

from pydantic import ValidationError

from src.models import Transaction, StoredTransactions
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

    def store_transactions(
        self, transactions: list[Transaction], bank_name: str, year: int, month: int
    ) -> None:
        dir_path = self.storage_dir_path / bank_name / str(year) / f"{month:02}"
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / "transactions.json"
        stored_transactions = StoredTransactions(transactions=transactions)

        with open(file_path, "w") as parsed_file:
            parsed_file.write(stored_transactions.model_dump_json())

    def get_transactions_for_bank_for_date(self, bank_name: str, year: int, month: int) -> list[Transaction]:
        file_path = self.storage_dir_path / bank_name / str(year) / f"{month:02}" / "transactions.json"

        try:
            with open(file_path) as parsed_file:
                json_data = json.load(parsed_file)

            stored_transactions = StoredTransactions(**json_data)
            return stored_transactions.transactions
        except FileNotFoundError:
            raise StorageServiceException(f"Could not find file at path: {file_path}")
        except ValidationError:
            raise StorageServiceException(f"Failed to convert json data into StoredTransactions object")

    def get_all_transactions_for_bank(self, bank_name: str) -> list[Transaction]:
        all_transactions_for_bank: list[Transaction] = []
        bank_dir_path = self.storage_dir_path / bank_name

        for year_dir_path in bank_dir_path.iterdir():
            year = year_dir_path.name

            for month_dir_path in (bank_dir_path / year).iterdir():
                month = month_dir_path.name

                transactions_for_bank_for_date = self.get_transactions_for_bank_for_date(
                    bank_name=bank_name, year=int(year), month=int(month)
                )
                all_transactions_for_bank.extend(transactions_for_bank_for_date)

        all_transactions_for_bank.sort(key=lambda t: t.date)
        return all_transactions_for_bank

    def get_all_transactions_for_date(self, year: int, month: int) -> list[Transaction]:
        all_transactions_for_date: list[Transaction] = []

        for bank_dir in self.storage_dir_path.iterdir():
            bank_name = bank_dir.name
            transactions_for_bank_for_date = self.get_transactions_for_bank_for_date(
                bank_name=bank_name, year=year, month=month
            )
            all_transactions_for_date.extend(transactions_for_bank_for_date)

        all_transactions_for_date.sort(key=lambda t: t.date)
        return all_transactions_for_date

    def get_all_transactions_for_bank_for_year(self, bank_name: str, year: int) -> list[Transaction]:
        all_transactions_for_bank_for_year: list[Transaction] = []
        bank_year_dir_path = self.storage_dir_path / bank_name / str(year)

        if not bank_year_dir_path.exists():
            return []

        for month_dir_path in bank_year_dir_path.iterdir():
            month = month_dir_path.name

            transactions_for_bank_for_date = self.get_transactions_for_bank_for_date(
                bank_name=bank_name, year=year, month=int(month)
            )
            all_transactions_for_bank_for_year.extend(transactions_for_bank_for_date)

        all_transactions_for_bank_for_year.sort(key=lambda t: t.date)
        return all_transactions_for_bank_for_year

    def get_all_transactions_for_year(self, year: int) -> list[Transaction]:
        all_transactions_for_year: list[Transaction] = []

        for bank_dir in self.storage_dir_path.iterdir():
            bank_name = bank_dir.name

            all_transactions_for_bank_for_year = self.get_all_transactions_for_bank_for_year(
                bank_name=bank_name, year=year
            )
            all_transactions_for_year.extend(all_transactions_for_bank_for_year)

        all_transactions_for_year.sort(key=lambda t: t.date)
        return all_transactions_for_year

    def get_all_transactions(self) -> list[Transaction]:
        all_transactions: list[Transaction] = []

        for bank_dir in self.storage_dir_path.iterdir():
            bank_name = bank_dir.name
            transactions_for_bank = self.get_all_transactions_for_bank(bank_name=bank_name)
            all_transactions.extend(transactions_for_bank)

        all_transactions.sort(key=lambda t: t.date)
        return all_transactions

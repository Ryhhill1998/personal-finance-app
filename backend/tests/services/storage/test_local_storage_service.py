import json
from datetime import date
from pathlib import Path

import pytest

from src.models import Transaction
from src.services.storage.local_storage_service import LocalStorageService
from src.services.storage.storage_service import StorageServiceException


@pytest.fixture
def local_storage_service(tmp_path) -> LocalStorageService:
    return LocalStorageService(tmp_path)


def test_store_statement_stores_expected_data_in_expected_location(
    tmp_path: Path, local_storage_service: LocalStorageService
) -> None:
    # ARRANGE
    statement_content = "PDF-1.4 fake content"

    # ACT
    local_storage_service.store_statement(
        statement_bytes=statement_content.encode("utf-8"), bank_name="Test Bank", year=2025, month=1
    )

    # ASSERT
    with open(tmp_path / "Test Bank" / "2025" / "01" / "statement.pdf") as statement_file:
        assert statement_file.read() == statement_content


def test_get_statement_for_bank_on_date_file_exists(tmp_path: Path, local_storage_service: LocalStorageService) -> None:
    # ARRANGE
    statement_content = "PDF-1.4 fake content"
    bank_name = "Test Bank"

    dir_path = tmp_path / bank_name / "2025" / "01"
    dir_path.mkdir(parents=True, exist_ok=True)
    statement_path = dir_path / "statement.pdf"
    statement_path.touch()
    statement_path.write_bytes(statement_content.encode("utf-8"))

    # ACT
    statement = local_storage_service.get_statement_for_bank_on_date(bank_name=bank_name, year=2025, month=1)

    # ASSERT
    assert statement == statement_content


def test_get_statement_for_bank_on_date_file_does_not_exist(local_storage_service: LocalStorageService) -> None:
    with pytest.raises(StorageServiceException, match="Could not find file at path: "):
        local_storage_service.get_statement_for_bank_on_date(bank_name="Test Bank", year=2025, month=1)


def test_store_transactions(tmp_path: Path, local_storage_service: LocalStorageService) -> None:
    # ARRANGE
    transactions = [
        Transaction(
            bank_name="Test Bank",
            date=date.fromisoformat("2025-01-01"),
            description="Transaction 1",
            amount_in=100,
            amount_out=0,
            balance=500,
        ),
        Transaction(
            bank_name="Test Bank",
            date=date.fromisoformat("2025-01-05"),
            description="Transaction 2",
            amount_in=0,
            amount_out=150,
            balance=350,
        ),
        Transaction(
            bank_name="Test Bank",
            date=date.fromisoformat("2025-01-21"),
            description="Transaction 3",
            amount_in=1000,
            amount_out=0,
            balance=1350,
        ),
    ]

    # ACT
    local_storage_service.store_transactions(transactions=transactions, bank_name="Test Bank", year=2025, month=1)

    # ASSERT
    expected_json_data = {
        "transactions": [
            {
                "bank_name": "Test Bank",
                "date": "2025-01-01",
                "description": "Transaction 1",
                "amount_in": 100,
                "amount_out": 0,
                "balance": 500,
            },
            {
                "bank_name": "Test Bank",
                "date": "2025-01-05",
                "description": "Transaction 2",
                "amount_in": 0,
                "amount_out": 150,
                "balance": 350,
            },
            {
                "bank_name": "Test Bank",
                "date": "2025-01-21",
                "description": "Transaction 3",
                "amount_in": 1000,
                "amount_out": 0,
                "balance": 1350,
            },
        ]
    }

    with open(tmp_path / "Test Bank" / "2025" / "01" / "transactions.json") as stored_transactions_file:
        json_data = json.load(stored_transactions_file)
        assert json_data == expected_json_data


def test_get_transactions_for_bank_for_date_file_exists(
    tmp_path: Path, local_storage_service: LocalStorageService
) -> None:
    # ARRANGE
    json_data = {
        "transactions": [
            {
                "bank_name": "Test Bank",
                "date": "2025-01-01",
                "description": "Transaction 1",
                "amount_in": 100,
                "amount_out": 0,
                "balance": 500,
            },
            {
                "bank_name": "Test Bank",
                "date": "2025-01-05",
                "description": "Transaction 2",
                "amount_in": 0,
                "amount_out": 150,
                "balance": 350,
            },
            {
                "bank_name": "Test Bank",
                "date": "2025-01-21",
                "description": "Transaction 3",
                "amount_in": 1000,
                "amount_out": 0,
                "balance": 1350,
            },
        ]
    }

    dir_path = tmp_path / "Test Bank" / "2025" / "01"
    dir_path.mkdir(parents=True, exist_ok=True)

    with open(dir_path / "transactions.json", "w") as stored_transactions_file:
        json.dump(json_data, stored_transactions_file)

    # ACT
    transactions = local_storage_service.get_transactions_for_bank_for_date(
        bank_name="Test Bank", year=2025, month=1
    )

    # ASSERT
    expected_transactions = [
        Transaction(
            bank_name="Test Bank",
            date=date.fromisoformat("2025-01-01"),
            description="Transaction 1",
            amount_in=100,
            amount_out=0,
            balance=500,
        ),
        Transaction(
            bank_name="Test Bank",
            date=date.fromisoformat("2025-01-05"),
            description="Transaction 2",
            amount_in=0,
            amount_out=150,
            balance=350,
        ),
        Transaction(
            bank_name="Test Bank",
            date=date.fromisoformat("2025-01-21"),
            description="Transaction 3",
            amount_in=1000,
            amount_out=0,
            balance=1350,
        ),
    ]
    assert transactions == expected_transactions


def test_get_transactions_for_bank_for_date_file_not_exists(local_storage_service: LocalStorageService) -> None:
    with pytest.raises(StorageServiceException, match="Could not find file at path: "):
        local_storage_service.get_transactions_for_bank_for_date(bank_name="Test Bank", year=2025, month=1)


def test_get_transactions_for_bank_for_date_data_cannot_be_parsed(
    tmp_path: Path, local_storage_service: LocalStorageService
) -> None:
    # ARRANGE
    json_data = {}

    dir_path = tmp_path / "Test Bank" / "2025" / "01"
    dir_path.mkdir(parents=True, exist_ok=True)

    with open(dir_path / "transactions.json", "w") as stored_transactions_file:
        json.dump(json_data, stored_transactions_file)

    # ACT & ASSERT
    with pytest.raises(StorageServiceException, match="Failed to convert json data into StoredTransactions object"):
        local_storage_service.get_transactions_for_bank_for_date(bank_name="Test Bank", year=2025, month=1)

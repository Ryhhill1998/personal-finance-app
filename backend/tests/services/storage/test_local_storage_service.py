import json
from datetime import date
from pathlib import Path

import pytest

from src.models import ParsedTransactions, Transaction
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
    with open(tmp_path / "Test Bank" / "raw" / f"Statement_2025_01.pdf") as statement_file:
        assert statement_file.read() == statement_content


def test_get_statement_file_exists(tmp_path: Path, local_storage_service: LocalStorageService) -> None:
    # ARRANGE
    statement_content = "PDF-1.4 fake content"
    bank_name = "Test Bank"

    dir_path = tmp_path / bank_name / "raw"
    dir_path.mkdir(parents=True, exist_ok=True)
    statement_path = dir_path / "Statement_2025_01.pdf"
    statement_path.touch()
    statement_path.write_bytes(statement_content.encode("utf-8"))

    # ACT
    statement = local_storage_service.get_statement(bank_name=bank_name, year=2025, month=1)

    # ASSERT
    assert statement == statement_content


def test_get_statement_file_does_not_exist(tmp_path: Path, local_storage_service: LocalStorageService) -> None:
    # ARRANGE
    statement_content = "PDF-1.4 fake content"
    bank_name = "Test Bank"

    dir_path = tmp_path / bank_name / "raw"
    dir_path.mkdir(parents=True, exist_ok=True)
    statement_path = dir_path / "Statement_2025_01.pdf"
    statement_path.touch()
    statement_path.write_bytes(statement_content.encode("utf-8"))

    # ACT
    statement = local_storage_service.get_statement(bank_name=bank_name, year=2025, month=1)

    # ASSERT
    assert statement == statement_content


def test_store_parsed_transactions(tmp_path: Path, local_storage_service: LocalStorageService) -> None:
    # ARRANGE
    parsed_transactions = ParsedTransactions(
        transactions=[
            Transaction(
                date=date.fromisoformat("2025-01-01"),
                description="Transaction 1",
                amount_in=100,
                amount_out=0,
                balance=500,
            ),
            Transaction(
                date=date.fromisoformat("2025-01-05"),
                description="Transaction 2",
                amount_in=0,
                amount_out=150,
                balance=350,
            ),
            Transaction(
                date=date.fromisoformat("2025-01-21"),
                description="Transaction 3",
                amount_in=1000,
                amount_out=0,
                balance=1350,
            ),
        ]
    )

    # ACT
    local_storage_service.store_parsed_transactions(
        parsed_transactions=parsed_transactions, bank_name="Test Bank", year=2025, month=1
    )

    # ASSERT
    expected_json_data = {
        "transactions": [
            {
                "date": "2025-01-01",
                "description": "Transaction 1",
                "amount_in": 100,
                "amount_out": 0,
                "balance": 500,
            },
            {
                "date": "2025-01-05",
                "description": "Transaction 2",
                "amount_in": 0,
                "amount_out": 150,
                "balance": 350,
            },
            {
                "date": "2025-01-21",
                "description": "Transaction 3",
                "amount_in": 1000,
                "amount_out": 0,
                "balance": 1350,
            },
        ]
    }

    with open(tmp_path / "Test Bank" / "parsed" / f"Statement_2025_01.json") as parsed_transactions_file:
        json_data = json.load(parsed_transactions_file)
        assert json_data == expected_json_data


def test_get_parsed_transactions_file_exists(tmp_path: Path, local_storage_service: LocalStorageService) -> None:
    # ARRANGE
    json_data = {
        "transactions": [
            {
                "date": "2025-01-01",
                "description": "Transaction 1",
                "amount_in": 100,
                "amount_out": 0,
                "balance": 500,
            },
            {
                "date": "2025-01-05",
                "description": "Transaction 2",
                "amount_in": 0,
                "amount_out": 150,
                "balance": 350,
            },
            {
                "date": "2025-01-21",
                "description": "Transaction 3",
                "amount_in": 1000,
                "amount_out": 0,
                "balance": 1350,
            },
        ]
    }

    dir_path = tmp_path / "Test Bank" / "parsed"
    dir_path.mkdir(parents=True, exist_ok=True)

    with open(dir_path / f"Statement_2025_01.json", "w") as parsed_transactions_file:
        json.dump(json_data, parsed_transactions_file)

    # ACT
    parsed_transactions = local_storage_service.get_parsed_transactions(bank_name="Test Bank", year=2025, month=1)

    # ASSERT
    expected_parsed_transactions = ParsedTransactions(
        transactions=[
            Transaction(
                date=date.fromisoformat("2025-01-01"),
                description="Transaction 1",
                amount_in=100,
                amount_out=0,
                balance=500,
            ),
            Transaction(
                date=date.fromisoformat("2025-01-05"),
                description="Transaction 2",
                amount_in=0,
                amount_out=150,
                balance=350,
            ),
            Transaction(
                date=date.fromisoformat("2025-01-21"),
                description="Transaction 3",
                amount_in=1000,
                amount_out=0,
                balance=1350,
            ),
        ]
    )
    assert parsed_transactions == expected_parsed_transactions


def test_get_parsed_transactions_file_not_exists(tmp_path: Path, local_storage_service: LocalStorageService) -> None:
    with pytest.raises(StorageServiceException, match="Could not find file at path: "):
        local_storage_service.get_parsed_transactions(bank_name="Test Bank", year=2025, month=1)

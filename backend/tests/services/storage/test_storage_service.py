from pathlib import Path

import pytest

from src.services.storage.local_storage_service import LocalStorageService


@pytest.fixture
def local_storage_service(tmp_path) -> LocalStorageService:
    return LocalStorageService(tmp_path)


def test_store_statement_stores_expected_data_in_expected_location(
    tmp_path: Path, local_storage_service: LocalStorageService
) -> None:
    # ARRANGE
    statement_bytes = "PDF-1.4 fake content".encode("utf-8")
    bank_name = "Test Bank"
    year = 2025
    month = 1

    # ACT
    local_storage_service.store_statement(statement_bytes=statement_bytes, bank_name=bank_name, year=year, month=month)

    # ASSERT
    with open(tmp_path / bank_name / "raw" / f"Statement_2025_01.pdf") as statement_file:
        assert statement_file.read() == "PDF-1.4 fake content"


def test_get_statement() -> None:
    pass


def test_store_parsed_transactions() -> None:
    pass


def test_get_parsed_transactions() -> None:
    pass

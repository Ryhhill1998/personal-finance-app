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
    statement_content = "PDF-1.4 fake content"

    # ACT
    local_storage_service.store_statement(
        statement_bytes=statement_content.encode("utf-8"), bank_name="Test Bank", year=2025, month=1
    )

    # ASSERT
    with open(tmp_path / "Test Bank" / "raw" / f"Statement_2025_01.pdf") as statement_file:
        assert statement_file.read() == statement_content


def test_get_statement(
    tmp_path: Path, local_storage_service: LocalStorageService
) -> None:
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


def test_store_parsed_transactions() -> None:
    pass


def test_get_parsed_transactions() -> None:
    pass

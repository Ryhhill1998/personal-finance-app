from datetime import date
from io import BytesIO
from pathlib import Path
from typing import Generator, Any

import pytest
from fastapi.testclient import TestClient

from src.dependencies import get_settings, get_model_statement_parser
from src.main import app
from src.models import Transaction
from src.settings import Settings


# -------------------- FIXTURES -------------------- #
@pytest.fixture
def override_get_model_service(tmp_path: Path) -> Generator[None, Any, None]:
    class MockModelService:
        async def parse_transactions(self, bank_name: str, statement: str) -> list[Transaction]:
            return [
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

    app.dependency_overrides[get_model_statement_parser] = lambda: MockModelService()
    yield

    app.dependency_overrides = {}


# -------------------- TESTS -------------------- #
def test_process_statement(tmp_path: Path, override_get_settings: None, override_get_model_service: None) -> None:
    # ARRANGE
    bank_name = "test_bank"
    year = 2025
    month = 9
    fake_statement = BytesIO(b"%PDF-1.4 fake content")
    client = TestClient(app)

    # ACT
    response = client.post(
        url=f"/statements/{bank_name}/{year}/{month}",
        files={"statement": (f"test_statement.pdf", fake_statement, "application/pdf")},
    )

    # ASSERT
    assert response.status_code == 200
    output_dir_path = tmp_path / bank_name / "2025" / "09"
    raw_file_path = output_dir_path / "statement.pdf"
    parsed_file_path = output_dir_path / "transactions.json"
    assert raw_file_path.is_file()
    assert parsed_file_path.is_file()

import json
from datetime import date
from io import BytesIO
from pathlib import Path
from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from src.dependencies import get_settings, get_model_statement_parser
from src.main import app
from src.models import Transaction
from src.settings import Settings


# -------------------- FIXTURES -------------------- #
@pytest.fixture
def override_get_settings(tmp_path: Path) -> Generator[None, Any, None]:
    test_settings = Settings(
        google_gen_ai_api_key="",
        google_gen_ai_model_name="",
        google_gen_ai_model_temp=1,
        google_gen_ai_model_max_tokens=8000,
        google_gen_ai_model_top_p=0.95,
        google_gen_ai_model_prompt_path=Path("src/prompt.txt"),
        local_storage_dir_path=tmp_path,
    )
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield

    app.dependency_overrides = {}


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
def test_get_bank_transactions_on_date(tmp_path: Path, override_get_settings: None) -> None:
    # ARRANGE
    bank_name = "Test Bank"
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

    dir_path = tmp_path / bank_name / "parsed"
    dir_path.mkdir(parents=True, exist_ok=True)

    with open(dir_path / f"Statement_2025_01.json", "w") as parsed_transactions_file:
        json.dump(json_data, parsed_transactions_file)

    client = TestClient(app)

    # ACT
    response = client.get(f"/transactions/bank/{bank_name}/2025/1")

    # ASSERT
    assert response.status_code == 200
    assert response.json() == json_data


def test_get_all_transactions_on_date():
    client = TestClient(app)
    response = client.get("/transactions/{year}/{month}")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_all_transactions():
    client = TestClient(app)
    response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_process_statement(tmp_path: Path, override_get_settings: None, override_get_model_service: None) -> None:
    # ARRANGE
    bank_name = "test_bank"
    year = 2025
    month = 9
    fake_statement = BytesIO(b"%PDF-1.4 fake content")
    client = TestClient(app)

    # ACT
    response = client.post(
        url=f"/process-statement/{bank_name}/{year}/{month}",
        files={"statement": (f"test_statement.pdf", fake_statement, "application/pdf")},
    )

    # ASSERT
    assert response.status_code == 200
    output_dir_path = tmp_path / bank_name / "2025" / "09"
    raw_file_path = output_dir_path / "statement.pdf"
    parsed_file_path = output_dir_path / "transactions.json"
    assert raw_file_path.is_file()
    assert parsed_file_path.is_file()

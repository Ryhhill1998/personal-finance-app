from io import BytesIO
from pathlib import Path
from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from src.dependencies import get_settings
from src.main import app
from src.settings import Settings


@pytest.fixture
def override_get_settings(tmp_path: Path) -> Generator[None, Any, None]:
    test_settings = Settings(
        google_gen_ai_api_key="",
        google_gen_ai_model_name="",
        google_gen_ai_model_temp=1,
        google_gen_ai_model_max_tokens=8000,
        google_gen_ai_model_top_p=0.95,
        google_gen_ai_model_prompt_path=Path("src/prompt.txt"),
        data_directory_path=tmp_path,
    )
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield

    app.dependency_overrides = {}


def test_get_bank_transactions_on_date():
    client = TestClient(app)
    response = client.get("/transactions/bank/{bank_name}/{year}/{month}")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


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


def test_process_statement(tmp_path: Path, override_get_settings):
    bank_name = "test_bank"
    year = 2025
    month = 9
    fake_statement = BytesIO(b"%PDF-1.4 fake content")
    client = TestClient(app)

    response = client.post(
        url=f"/process-statement/{bank_name}/{year}/{month}",
        files={"statement": (f"test_statement.pdf", fake_statement, "application/pdf")},
    )

    assert response.status_code == 200
    output_dir_path = tmp_path / bank_name
    expected_file_name = f"Statement_{year}_{month}"
    raw_file_path = output_dir_path / "raw" / f"{expected_file_name}.pdf"
    parsed_file_path = output_dir_path / "parsed" / f"{expected_file_name}.json"
    assert raw_file_path.is_file()
    # assert parsed_file_path.is_file()

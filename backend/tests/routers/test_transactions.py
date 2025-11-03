import json
from pathlib import Path

from fastapi.testclient import TestClient

from src.main import app


def test_get_bank_transactions_for_date(tmp_path: Path, override_get_settings: None) -> None:
    # ARRANGE
    bank_name = "Test Bank"
    transactions_list = [
        {
            "bank_name": bank_name,
            "date": "2025-01-01",
            "description": "Transaction 1",
            "amount_in": 100,
            "amount_out": 0,
            "balance": 500,
        },
        {
            "bank_name": bank_name,
            "date": "2025-01-05",
            "description": "Transaction 2",
            "amount_in": 0,
            "amount_out": 150,
            "balance": 350,
        },
        {
            "bank_name": bank_name,
            "date": "2025-01-21",
            "description": "Transaction 3",
            "amount_in": 1000,
            "amount_out": 0,
            "balance": 1350,
        },
    ]
    json_data = {"transactions": transactions_list}

    dir_path = tmp_path / bank_name / "2025" / "01"
    dir_path.mkdir(parents=True, exist_ok=True)

    with open(dir_path / "transactions.json", "w") as parsed_transactions_file:
        json.dump(json_data, parsed_transactions_file)

    client = TestClient(app)

    # ACT
    response = client.get(f"/transactions/?bank_name={bank_name}&year=2025&month=1")

    # ASSERT
    assert response.status_code == 200
    assert response.json() == transactions_list


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

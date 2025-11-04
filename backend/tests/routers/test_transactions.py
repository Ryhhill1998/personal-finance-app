from fastapi.testclient import TestClient

from src.main import app


def test_get_bank_transactions_for_date(mock_data: None, override_get_settings: None) -> None:
    # ARRANGE
    bank_name = "barclays"
    client = TestClient(app)

    # ACT
    response = client.get(f"/transactions/?bank_name={bank_name}&year=2025&month=1")

    # ASSERT
    expected_transactions = [
        {
            "bank_name": "Barclays",
            "date": "2025-01-03",
            "description": "Grocery Store",
            "amount_in": 0,
            "amount_out": 75.20,
            "balance": 1924.80
        },
        {
            "bank_name": "Barclays",
            "date": "2025-01-10",
            "description": "Salary",
            "amount_in": 2500,
            "amount_out": 0,
            "balance": 4424.80
        },
        {
            "bank_name": "Barclays",
            "date": "2025-01-25",
            "description": "Electric Bill",
            "amount_in": 0,
            "amount_out": 120.50,
            "balance": 4304.30
        }
    ]
    assert response.status_code == 200
    assert response.json() == expected_transactions


def test_get_all_transactions_for_bank(mock_data: None, override_get_settings: None):
    # ARRANGE
    bank_name = "lloyds"
    client = TestClient(app)

    # ACT
    response = client.get(f"/transactions/?bank_name={bank_name}")

    # ASSERT
    expected_transactions = [
        {
            "bank_name": "Lloyds",
            "date": "2024-12-15",
            "description": "Christmas Shopping",
            "amount_in": 0,
            "amount_out": 300,
            "balance": 1800.00
        },
        {
            "bank_name": "Lloyds",
            "date": "2024-12-31",
            "description": "New Year Deposit",
            "amount_in": 500,
            "amount_out": 0,
            "balance": 2300.00
        },
        {
            "bank_name": "Lloyds",
            "date": "2025-01-05",
            "description": "Restaurant",
            "amount_in": 0,
            "amount_out": 80.00,
            "balance": 2200.00
        },
        {
            "bank_name": "Lloyds",
            "date": "2025-01-20",
            "description": "Freelance Payment",
            "amount_in": 600,
            "amount_out": 0,
            "balance": 2800.00
        }
    ]
    assert response.status_code == 200
    assert response.json() == expected_transactions


def test_get_all_transactions_for_date(mock_data: None, override_get_settings: None):
    # ARRANGE
    client = TestClient(app)

    # ACT
    response = client.get("/transactions/?year=2025&month=1")

    # ASSERT
    expected_transactions = [
        {
            "bank_name": "Barclays",
            "date": "2025-01-03",
            "description": "Grocery Store",
            "amount_in": 0,
            "amount_out": 75.20,
            "balance": 1924.80
        },
        {
            "bank_name": "Lloyds",
            "date": "2025-01-05",
            "description": "Restaurant",
            "amount_in": 0,
            "amount_out": 80.00,
            "balance": 2200.00
        },
        {
            "bank_name": "Monzo",
            "date": "2025-01-08",
            "description": "Online Subscription",
            "amount_in": 0,
            "amount_out": 12.99,
            "balance": 987.01
        },
        {
            "bank_name": "Barclays",
            "date": "2025-01-10",
            "description": "Salary",
            "amount_in": 2500,
            "amount_out": 0,
            "balance": 4424.80
        },
        {
            "bank_name": "Monzo",
            "date": "2025-01-16",
            "description": "Gift Received",
            "amount_in": 50,
            "amount_out": 0,
            "balance": 1037.01
        },
        {
            "bank_name": "Lloyds",
            "date": "2025-01-20",
            "description": "Freelance Payment",
            "amount_in": 600,
            "amount_out": 0,
            "balance": 2800.00
        },
        {
            "bank_name": "Barclays",
            "date": "2025-01-25",
            "description": "Electric Bill",
            "amount_in": 0,
            "amount_out": 120.50,
            "balance": 4304.30
        },
        {
            "bank_name": "Monzo",
            "date": "2025-01-30",
            "description": "Groceries",
            "amount_in": 0,
            "amount_out": 47.85,
            "balance": 989.16
        }
    ]
    assert response.status_code == 200
    assert response.json() == expected_transactions


def test_get_all_transactions(mock_data: None, override_get_settings: None):
    # ARRANGE
    client = TestClient(app)

    # ACT
    response = client.get("/transactions")

    # ASSERT
    expected_transactions = [
        {
            "bank_name": "Lloyds",
            "date": "2024-12-15",
            "description": "Christmas Shopping",
            "amount_in": 0,
            "amount_out": 300,
            "balance": 1800.00
        },
        {
            "bank_name": "Lloyds",
            "date": "2024-12-31",
            "description": "New Year Deposit",
            "amount_in": 500,
            "amount_out": 0,
            "balance": 2300.00
        },
        {
            "bank_name": "Barclays",
            "date": "2025-01-03",
            "description": "Grocery Store",
            "amount_in": 0,
            "amount_out": 75.20,
            "balance": 1924.80
        },
        {
            "bank_name": "Lloyds",
            "date": "2025-01-05",
            "description": "Restaurant",
            "amount_in": 0,
            "amount_out": 80.00,
            "balance": 2200.00
        },
        {
            "bank_name": "Monzo",
            "date": "2025-01-08",
            "description": "Online Subscription",
            "amount_in": 0,
            "amount_out": 12.99,
            "balance": 987.01
        },
        {
            "bank_name": "Barclays",
            "date": "2025-01-10",
            "description": "Salary",
            "amount_in": 2500,
            "amount_out": 0,
            "balance": 4424.80
        },
        {
            "bank_name": "Monzo",
            "date": "2025-01-16",
            "description": "Gift Received",
            "amount_in": 50,
            "amount_out": 0,
            "balance": 1037.01
        },
        {
            "bank_name": "Lloyds",
            "date": "2025-01-20",
            "description": "Freelance Payment",
            "amount_in": 600,
            "amount_out": 0,
            "balance": 2800.00
        },
        {
            "bank_name": "Barclays",
            "date": "2025-01-25",
            "description": "Electric Bill",
            "amount_in": 0,
            "amount_out": 120.50,
            "balance": 4304.30
        },
        {
            "bank_name": "Monzo",
            "date": "2025-01-30",
            "description": "Groceries",
            "amount_in": 0,
            "amount_out": 47.85,
            "balance": 989.16
        },
        {
            "bank_name": "Barclays",
            "date": "2025-02-02",
            "description": "Gym Membership",
            "amount_in": 0,
            "amount_out": 45.00,
            "balance": 4259.30
        },
        {
            "bank_name": "Barclays",
            "date": "2025-02-18",
            "description": "Bonus",
            "amount_in": 500,
            "amount_out": 0,
            "balance": 4759.30
        }
    ]
    assert response.status_code == 200
    assert response.json() == expected_transactions


def test_get_all_transactions(mock_data: None, override_get_settings: None):
    # ARRANGE
    client = TestClient(app)

    # ACT
    response = client.get("/transactions")

    # ASSERT
    expected_transactions = [
        {
            "bank_name": "Lloyds",
            "date": "2024-12-15",
            "description": "Christmas Shopping",
            "amount_in": 0,
            "amount_out": 300,
            "balance": 1800.00
        },
        {
            "bank_name": "Lloyds",
            "date": "2024-12-31",
            "description": "New Year Deposit",
            "amount_in": 500,
            "amount_out": 0,
            "balance": 2300.00
        },
        {
            "bank_name": "Barclays",
            "date": "2025-01-03",
            "description": "Grocery Store",
            "amount_in": 0,
            "amount_out": 75.20,
            "balance": 1924.80
        },
        {
            "bank_name": "Lloyds",
            "date": "2025-01-05",
            "description": "Restaurant",
            "amount_in": 0,
            "amount_out": 80.00,
            "balance": 2200.00
        },
        {
            "bank_name": "Monzo",
            "date": "2025-01-08",
            "description": "Online Subscription",
            "amount_in": 0,
            "amount_out": 12.99,
            "balance": 987.01
        },
        {
            "bank_name": "Barclays",
            "date": "2025-01-10",
            "description": "Salary",
            "amount_in": 2500,
            "amount_out": 0,
            "balance": 4424.80
        },
        {
            "bank_name": "Monzo",
            "date": "2025-01-16",
            "description": "Gift Received",
            "amount_in": 50,
            "amount_out": 0,
            "balance": 1037.01
        },
        {
            "bank_name": "Lloyds",
            "date": "2025-01-20",
            "description": "Freelance Payment",
            "amount_in": 600,
            "amount_out": 0,
            "balance": 2800.00
        },
        {
            "bank_name": "Barclays",
            "date": "2025-01-25",
            "description": "Electric Bill",
            "amount_in": 0,
            "amount_out": 120.50,
            "balance": 4304.30
        },
        {
            "bank_name": "Monzo",
            "date": "2025-01-30",
            "description": "Groceries",
            "amount_in": 0,
            "amount_out": 47.85,
            "balance": 989.16
        },
        {
            "bank_name": "Barclays",
            "date": "2025-02-02",
            "description": "Gym Membership",
            "amount_in": 0,
            "amount_out": 45.00,
            "balance": 4259.30
        },
        {
            "bank_name": "Barclays",
            "date": "2025-02-18",
            "description": "Bonus",
            "amount_in": 500,
            "amount_out": 0,
            "balance": 4759.30
        }
    ]
    assert response.status_code == 200
    assert response.json() == expected_transactions

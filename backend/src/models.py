from datetime import date

from pydantic import BaseModel


class Transaction(BaseModel):
    date: date
    description: str
    amount_in: float
    amount_out: float
    balance: float


class ParsedTransactions(BaseModel):
    transactions: list[Transaction]
    bank_name: str
    year: int
    month: int

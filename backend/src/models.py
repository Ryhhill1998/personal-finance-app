from datetime import date

from pydantic import BaseModel


class ParsedTransaction(BaseModel):
    date: date
    description: str
    amount_in: float
    amount_out: float
    balance: float


class Transaction(ParsedTransaction):
    bank_name: str

    @staticmethod
    def from_parsed_transaction(bank_name: str, parsed_transaction: ParsedTransaction) -> "Transaction":
        return Transaction(
            bank_name=bank_name,
            date=parsed_transaction.date,
            description=parsed_transaction.description,
            amount_in=parsed_transaction.amount_in,
            amount_out=parsed_transaction.amount_out,
            balance=parsed_transaction.balance,
        )


class StoredTransactions(BaseModel):
    transactions: list[Transaction]

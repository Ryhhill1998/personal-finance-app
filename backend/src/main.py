from typing import Annotated

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.params import Depends

from src.dependencies import get_model_statement_parser, get_local_storage_service
from src.models import Transaction
from src.services.statement_parser.model_statement_parser import ModelStatementParser
from src.services.storage.storage_service import StorageService, StorageServiceException

app = FastAPI()


@app.get("/")
async def health_check():
    return {"status": "running"}


@app.get("/transactions")
async def get_all_transactions_for_all_banks():
    """
    Gets all transactions for all banks for all dates.
    If no data exists, raises a 404 Not Found error.
    """

    return {"transactions": []}


@app.get("/transactions/bank/{bank_name}")
async def get_all_transactions_for_bank(year: int, month: int):
    """
    Gets all transactions for all banks for a specific year and month.
    If no data exists, raises a 404 Not Found error.
    """

    return {"transactions": []}


@app.get("/transactions/{year}/{month}")
async def get_transactions_for_all_banks_for_date(year: int, month: int):
    """
    Gets all transactions for all banks for a specific year and month.
    If no data exists, raises a 404 Not Found error.
    """

    return {"transactions": []}


@app.get("/transactions/bank/{bank_name}/{year}/{month}")
async def get_transactions_for_bank_for_date(
    bank_name: str,
    year: int,
    month: int,
    storage_service: Annotated[StorageService, Depends(get_local_storage_service)]
) -> list[Transaction]:
    """
    Gets all transactions for a specific bank for a specific year and month.
    If no data exists, raises a 404 Not Found error.
    """

    try:
        return storage_service.get_transactions_for_bank_for_date(bank_name=bank_name, year=year, month=month)
    except StorageServiceException:
        raise HTTPException(status_code=404, detail="Cannot find requested file")


@app.post("/process-statement/{bank_name}/{year}/{month}")
async def process_statement(
    bank_name: str,
    year: int,
    month: int,
    statement: UploadFile,
    statement_parser: Annotated[ModelStatementParser, Depends(get_model_statement_parser)],
    storage_service: Annotated[StorageService, Depends(get_local_storage_service)],
):
    """
    Processes the uploaded statement and stores the result.
    Also stores the raw uploaded file.
    Does not return the result - this must be retrieved by one of the above GET methods.
    """

    # extract bytes from uploaded statement
    statement_bytes = statement.file.read()

    # store uploaded statement
    storage_service.store_statement(statement_bytes=statement_bytes, bank_name=bank_name, year=year, month=month)

    # get json data from pdf via model
    transactions = await statement_parser.parse_transactions(bank_name=bank_name, statement=statement_bytes.decode())

    # store parsed transactions
    storage_service.store_transactions(
        transactions=transactions, bank_name=bank_name, year=year, month=month
    )

from typing import Annotated

from fastapi import FastAPI, UploadFile
from fastapi.params import Depends

from src.dependencies import get_settings
from src.settings import Settings

app = FastAPI()


@app.get("/")
async def root(settings: Annotated[Settings, Depends(get_settings)]):
    print(settings)
    return {"message": "Hello World"}


@app.get("/transactions/bank/{bank_name}/{year}/{month}")
async def get_bank_transactions_on_date(bank: str, year: int, month: int):
    """
    Gets all transactions for a specific bank for a specific year and month.
    If no data exists, raises a 404 Not Found error.
    """

    return {"transactions": []}


@app.get("/transactions/{year}/{month}")
async def get_all_transactions_on_date(year: int, month: int):
    """
    Gets all transactions for all banks for a specific year and month.
    If no data exists, raises a 404 Not Found error.
    """

    return {"transactions": []}


@app.get("/transactions")
async def get_all_transactions():
    """
    Gets all transactions for all banks for all dates.
    If no data exists, raises a 404 Not Found error.
    """

    return {"transactions": []}


@app.post("/process-statement/{bank_name}/{year}/{month}")
async def process_statement(bank_name: str, year: int, month: int, statement: UploadFile):
    """
    Processes the uploaded statement and stores the result.
    Does not return the result - this must be retrieved by one of the above GET methods.
    """
    print(statement.filename)

    return {"status": "processing"}

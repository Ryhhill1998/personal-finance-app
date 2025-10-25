import json
from typing import Annotated

from fastapi import FastAPI, UploadFile
from fastapi.params import Depends

from src.dependencies import get_settings, get_model_service
from src.services.statement_parser.model_statement_parser import ModelStatementParser
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
async def process_statement(
    bank_name: str,
    year: int,
    month: int,
    statement: UploadFile,
    settings: Annotated[Settings, Depends(get_settings)],
    model_service: Annotated[ModelStatementParser, Depends(get_model_service)],
):
    """
    Processes the uploaded statement and stores the result.
    Also stores the raw uploaded file.
    Does not return the result - this must be retrieved by one of the above GET methods.
    """

    output_dir_path = settings.data_directory_path / bank_name
    output_file_name = f"Statement_{year}_{month}"
    raw_dir_path = output_dir_path / "raw"
    parsed_dir_path = output_dir_path / "parsed"
    raw_dir_path.mkdir(parents=True, exist_ok=True)
    parsed_dir_path.mkdir(parents=True, exist_ok=True)
    raw_file_path = raw_dir_path / f"{output_file_name}.pdf"
    parsed_file_path = parsed_dir_path / f"{output_file_name}.json"
    statement_bytes = statement.file.read()
    raw_file_path.write_bytes(statement_bytes)

    # get json data from pdf via model
    parsed_transactions = await model_service.parse_transactions(statement_bytes.decode())

    with open(parsed_file_path, "w") as parsed_file:
        json.dump(parsed_transactions.model_dump_json(), parsed_file)

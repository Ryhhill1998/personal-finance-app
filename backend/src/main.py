from typing import Annotated

from fastapi import FastAPI
from fastapi.params import Depends

from src.dependencies import get_settings
from src.settings import Settings

app = FastAPI()


@app.get("/")
async def root(settings: Annotated[Settings, Depends(get_settings)]):
    print(settings)
    return {"message": "Hello World"}


@app.get("/transactions/{bank}/{year}/{month}")
async def get_bank_transactions_on_date(bank: str, year: int, month: int):
    return {"transactions": []}


@app.get("/transactions/{year}/{month}")
async def get_all_transactions_on_date(year: int, month: int):
    return {"transactions": []}


@app.get("/transactions")
async def get_all_transactions():
    return {"transactions": []}


@app.post("/process-statement")
async def process_statement(statement: dict):
    return {"status": "processing"}

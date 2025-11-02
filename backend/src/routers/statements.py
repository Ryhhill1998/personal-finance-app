from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends

from src.dependencies import get_local_storage_service, get_model_statement_parser
from src.services.statement_parser.model_statement_parser import ModelStatementParser
from src.services.storage.storage_service import StorageService

router = APIRouter(prefix="/statements")


@router.post("/{bank_name}/{year}/{month}")
async def upload_statement(
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

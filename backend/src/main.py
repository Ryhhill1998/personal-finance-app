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

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_local_storage_service
from src.models import Transaction
from src.services.storage.storage_service import StorageService, StorageServiceException

router = APIRouter(prefix="/transactions")


@router.get("/")
async def get_all_transactions_for_all_banks():
    """
    Gets all transactions for all banks for all dates.
    If no data exists, raises a 404 Not Found error.
    """

    return {"transactions": []}


@router.get("/bank/{bank_name}")
async def get_all_transactions_for_bank(year: int, month: int):
    """
    Gets all transactions for all banks for a specific year and month.
    If no data exists, raises a 404 Not Found error.
    """

    return {"transactions": []}


@router.get("/{year}/{month}")
async def get_transactions_for_all_banks_for_date(year: int, month: int):
    """
    Gets all transactions for all banks for a specific year and month.
    If no data exists, raises a 404 Not Found error.
    """

    return {"transactions": []}


@router.get("/")
async def get_transactions(
    storage_service: Annotated[StorageService, Depends(get_local_storage_service)],
    bank_name: str | None = None,
    year: int | None = None,
    month: int | None = None,
) -> list[Transaction]:
    """
    Gets requested transactions.

    Query parameters:
    - bank_name: optional, filter by bank
    - year: optional, filter by year (requires month if month is provided)
    - month: optional, filter by month (requires year)

    If no data exists, raises a 404 Not Found error.
    """

    try:
        if bank_name is not None and year is not None and month is not None:
            return storage_service.get_transactions_for_bank_for_date(bank_name=bank_name, year=year, month=month)
        elif bank_name is not None and year is not None:
            return storage_service.get_all_transactions_for_bank_for_year(bank_name=bank_name, year=year)
        elif bank_name is not None:
            return storage_service.get_all_transactions_for_bank(bank_name)
        elif year is not None and month is not None:
            return storage_service.get_all_transactions_for_date(year=year, month=month)
        elif year is not None:
            return storage_service.get_all_transactions_for_year(year)
        elif bank_name is None and year is None and month is None:
            return storage_service.get_all_transactions()
        else:
            raise HTTPException(status_code=400, detail="Invalid bank_name, year, month combination")
    except StorageServiceException:
        raise HTTPException(status_code=404, detail="Cannot find requested file")

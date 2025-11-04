from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_local_storage_service
from src.models import Transaction
from src.services.storage.storage_service import StorageService, StorageServiceException, \
    StorageServiceNotFoundException

router = APIRouter(prefix="/transactions")


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
        if bank_name is None and year is None and month is None:
            return storage_service.get_all_transactions()

        if bank_name is not None and year is None and month is None:
            return storage_service.get_all_transactions_for_bank(bank_name)

        if bank_name is not None and year is not None and month is None:
            return storage_service.get_all_transactions_for_bank_for_year(bank_name=bank_name, year=year)

        if bank_name is not None and year is not None and month is not None:
            return storage_service.get_transactions_for_bank_for_date(bank_name=bank_name, year=year, month=month)

        if bank_name is None and year is not None and month is None:
            return storage_service.get_all_transactions_for_year(year)

        if bank_name is None and year is not None and month is not None:
            return storage_service.get_all_transactions_for_date(year=year, month=month)

        raise HTTPException(status_code=400, detail="Invalid bank_name, year, month combination")
    except StorageServiceNotFoundException:
        raise HTTPException(status_code=404, detail="Cannot find requested file")
    except StorageServiceException:
        raise HTTPException(status_code=500, detail="Invalid file")

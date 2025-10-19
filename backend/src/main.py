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

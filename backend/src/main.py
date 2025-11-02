from fastapi import FastAPI

from src.routers import transactions, statements

app = FastAPI()

app.include_router(transactions.router)
app.include_router(statements.router)


@app.get("/")
async def health_check():
    return {"status": "running"}

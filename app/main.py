from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.core import create_tables # ,drop_tables

from app.routers.transaction import router as transaction_router
from app.routers.get_transaction import router as get_transaction


@asynccontextmanager
async def lifespan(app: FastAPI):
#    await drop_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(transaction_router)
app.include_router(get_transaction)
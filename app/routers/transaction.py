from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models import Transaction
from app.schemas.transaction_schema import TransactionCreate


router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("", response_model=TransactionCreate)
async def create_transaction(
    data: Annotated[TransactionCreate, Depends()],
    session: AsyncSession = Depends(get_db)
):
    transaction = Transaction(
        amount=data.amount,
        type=data.type
    )

    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)

    return transaction
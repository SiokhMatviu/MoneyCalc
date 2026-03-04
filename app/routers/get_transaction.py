from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import Transaction
from datetime import datetime, timedelta
from sqlalchemy import select, func, case

from app.schemas.transaction_schema import TransactionRead, TransactionsWithTotals, MonthStats, TotalStats

router = APIRouter(prefix="/get_transaction", tags=["get_transaction"])


@router.get("/stats/day", response_model=TransactionsWithTotals)
async def get_transactions(
    day: int = Query(...),
    month: int = Query(...),
    year: int = Query(...),
    session: AsyncSession = Depends(get_db)
):
    date = datetime(year, month, day)
    start = datetime.combine(date, datetime.min.time())
    end = start + timedelta(days=1)


    stmt = select(Transaction).where(
        Transaction.created_at >= start,
        Transaction.created_at < end
    )

    result = await session.execute(stmt)
    transactions = result.scalars().all()


    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    daily_balance = total_income - total_expense


    transactions_read = [
        TransactionRead(
            amount=t.amount,
            type=t.type,
            created_at=t.created_at
        ) for t in transactions
    ]


    return TransactionsWithTotals(
        date=date,
        transactions=transactions_read,
        total_income=total_income,
        total_expense=total_expense,
        daily_balance=daily_balance
    )


@router.get("/stats/month", response_model=MonthStats)
async def get_month_stats(
    year: int = Query(..., description="Рік для статистики", examples={"example1": {"summary": "2026", "value": 2026}}),
    month: int = Query(..., description="Місяць для статистики", examples={"example1": {"summary": "Лютий", "value": 2}}),
    session: AsyncSession = Depends(get_db)
):

    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)


    stmt = select(Transaction).where(
        Transaction.created_at >= start,
        Transaction.created_at < end
    )
    result = await session.execute(stmt)
    transactions = result.scalars().all()


    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    monthly_balance = total_income - total_expense


    return MonthStats(
        year=year,
        month=month,
        total_income=total_income,
        total_expense=total_expense,
        monthly_balance=monthly_balance
    )


@router.get("/stats/total", response_model=TotalStats)
async def get_total_stats(session: AsyncSession = Depends(get_db)):
    # Використовуємо SUM прямо в SQL
    stmt = select(
        func.coalesce(func.sum(case((Transaction.type == "income", Transaction.amount), else_=0)), 0),
        func.coalesce(func.sum(case((Transaction.type == "expense", Transaction.amount), else_=0)), 0)
    )
    result = await session.execute(stmt)
    total_income, total_expense = result.one()

    balance = total_income - total_expense

    return TotalStats(
        total_income=total_income,
        total_expense=total_expense,
        balance=balance
    )
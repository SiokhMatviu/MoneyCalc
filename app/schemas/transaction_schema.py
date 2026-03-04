from decimal import Decimal
from pydantic import BaseModel, condecimal
from app.schemas.enum_schema import TransactionType
from typing import Annotated, List
from datetime import date, datetime


class TransactionCreate(BaseModel):
    amount: Annotated[Decimal, condecimal(gt=0)]
    type: TransactionType


class TransactionRead(BaseModel):
    amount: Decimal
    type: str
    created_at: datetime


class TransactionsWithTotals(BaseModel):
    date: date
    transactions: List[TransactionRead]
    total_income: Decimal
    total_expense: Decimal
    daily_balance: Decimal


class MonthStats(BaseModel):
    year: int
    month: int
    total_income: Decimal
    total_expense: Decimal
    monthly_balance: Decimal


class TotalStats(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
from datetime import datetime
from decimal import Decimal
from app.schemas.enum_schema import TransactionType
from sqlalchemy import DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(nullable=False)
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

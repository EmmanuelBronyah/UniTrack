from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func, Numeric
from src.database.db import Base
from datetime import date
from datetime import datetime
from decimal import Decimal


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_number: Mapped[str] = mapped_column(String(7), unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, service_number={self.service_number!r})"


class EmployeeRecord(Base):
    __tablename__ = "employee_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_number: Mapped[str] = mapped_column(index=True, unique=True)
    name: Mapped[str] = mapped_column(index=True)
    unit: Mapped[str] = mapped_column(index=True)
    grade: Mapped[str] = mapped_column(index=True)
    appointment_date: Mapped[date] = mapped_column(nullable=True)
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False, default=0.0000
    )
    amount_deducted: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False, default=0.0000
    )
    outstanding_difference: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False, default=0.0000
    )
    full_payment: Mapped[bool] = mapped_column(default=False)
    no_payment: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"EmployeeRecords(id={self.id!r}, name={self.name!r}, unit={self.unit!r}, grade={self.grade!r}, total_amount={self.total_amount!r}, amount_deducted={self.amount_deducted!r}, outstanding_difference={self.outstanding_difference!r})"

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, ForeignKey, Numeric
from src.api.database.db import Base
from datetime import datetime
from decimal import Decimal


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_number: Mapped[str] = mapped_column(String(7), unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    # Relationships
    employee_records: Mapped[list["EmployeeRecord"]] = relationship(
        back_populates="created_by"
    )
    updated_records: Mapped[list["EmployeeRecord"]] = relationship(
        back_populates="updated_by",
        foreign_keys=lambda: [EmployeeRecord.updated_by_id],
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, service_number={self.service_number!r})"


class EmployeeRecord(Base):
    __tablename__ = "employee_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    unit: Mapped[str] = mapped_column(index=True)
    grade: Mapped[str] = mapped_column(index=True)
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False, default=0.0000
    )
    remaining_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False, default=0.0000
    )
    outstanding_difference: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False, default=0.0000
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    created_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_by: Mapped["User"] = relationship(back_populates="employee_records")

    updated_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    updated_by: Mapped["User"] = relationship(
        back_populates="updated_records", foreign_keys=[updated_by_id]
    )

    def __repr__(self) -> str:
        return f"EmployeeRecords(id={self.id!r}, name={self.name!r}, unit={self.unit!r}, grade={self.grade!r}, total_amount={self.total_amount!r}, remaining_amount={self.remaining_amount!r}, outstanding_difference={self.outstanding_difference!r})"

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, Numeric, ForeignKey
from src.database.db import Base
from datetime import date
from datetime import datetime
from decimal import Decimal


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_number: Mapped[str] = mapped_column(String(7), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, service_number={self.service_number!r})"


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    # Relationships
    employees: Mapped[list["Employee"]] = relationship(back_populates="unit")

    def __repr__(self) -> str:
        return f"Unit(id={self.id!r}, name={self.name!r})"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Relationships
    employees: Mapped[list["Employee"]] = relationship(back_populates="grade")

    def __repr__(self) -> str:
        return f"Grade(id={self.id!r}, name={self.name!r})"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Relationships
    employees: Mapped[list["Employee"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r})"


class Gender(Base):
    __tablename__ = "genders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    # Relationships
    employees: Mapped[list["Employee"]] = relationship(back_populates="gender")

    def __repr__(self) -> str:
        return f"Gender(id={self.id!r}, name={self.name!r})"


class Rank(Base):
    __tablename__ = "ranks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    # Relationships
    employees: Mapped[list["Employee"]] = relationship(back_populates="rank")

    def __repr__(self) -> str:
        return f"Rank(id={self.id!r}, name={self.name!r})"


class DeductionStatus(Base):
    __tablename__ = "deduction_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Relationships
    occurrences: Mapped[list["Occurrence"]] = relationship(
        back_populates="deduction_status"
    )

    def __repr__(self) -> str:
        return f"DeductionStatus(id={self.id!r}, name={self.name!r})"


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_number: Mapped[str] = mapped_column(String(7), index=True, unique=True)
    name: Mapped[str] = mapped_column(index=True)
    gender_id: Mapped[int] = mapped_column(ForeignKey("genders.id"))
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    grade_id: Mapped[int] = mapped_column(ForeignKey("grades.id"))
    rank_id: Mapped[int] = mapped_column(ForeignKey("ranks.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    total_amount_deducted: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False, default=0.00
    )

    # Relationships
    gender: Mapped["Gender"] = relationship(back_populates="employees")
    unit: Mapped["Unit"] = relationship(back_populates="employees")
    grade: Mapped["Grade"] = relationship(back_populates="employees")
    rank: Mapped["Rank"] = relationship(back_populates="employees")
    category: Mapped["Category"] = relationship(back_populates="employees")
    occurrences: Mapped[list["Occurrence"]] = relationship(
        back_populates="employee", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Employee(id={self.id!r}, service_number={self.service_number!r})"


class Occurrence(Base):
    __tablename__ = "occurrences"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE")
    )
    uniform_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False, default=0.00
    )
    amount_deducted: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False, default=0.00
    )
    outstanding_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False, default=0.00
    )
    deduction_status_id: Mapped[int] = mapped_column(
        ForeignKey("deduction_statuses.id")
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="occurrences")
    deduction_status: Mapped["DeductionStatus"] = relationship(
        back_populates="occurrences"
    )

    def __repr__(self) -> str:
        return f"Occurrence(id={self.id!r}, employee_id={self.employee_id!r})"

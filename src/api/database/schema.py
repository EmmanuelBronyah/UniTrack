from pydantic import BaseModel, Field


class UserBase(BaseModel):
    service_number: str = Field(max_length=7)
    username: str


class UserCreate(UserBase):
    password: str


class EmployeeRecord(BaseModel):
    service_number: str
    name: str
    unit: str
    grade: str
    total_amount: float
    remaining_amount: float
    outstanding_difference: float

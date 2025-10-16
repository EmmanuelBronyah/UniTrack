from src.database.db import SessionLocal
from src.database.models import Unit, Grade, Category, Gender, DeductionStatus, Rank


units = ["5 BN", "4 BN", "6 BN", "37 MIL HOSP", "66 ARTY REGT"]
grades = [
    "Programmer",
    "Senior Executive Officer",
    "Higher Executive Officer",
    "Executive Officer",
    "Pharmacist",
]
categories = [
    "ARTISAN",
    "LABOURER",
    "EXECUTIVE OFFICER",
    "ADMINISTRATIVE OFFICER",
    "MEDICAL OFFICER",
]
gender = ["Male", "Female"]
deduction_status = ["Full Deduction", "Partial Deduction", "No Deduction"]
rank = ["Junior", "Senior"]

with SessionLocal() as db:
    for unit in units:
        db.add(Unit(name=unit))

    for grade in grades:
        db.add(Grade(name=grade))

    for category in categories:
        db.add(Category(name=category))

    for name in gender:
        db.add(Gender(name=name))

    for name in deduction_status:
        db.add(DeductionStatus(name=name))

    for name in rank:
        db.add(Rank(name=name))

    db.commit()

print("✅ Database prefilled successfully!")

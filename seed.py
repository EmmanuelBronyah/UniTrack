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
    "Artisan",
    "Chief Yard Foreman",
    "Driver",
    "Field Worker",
    "General",
    "Labourer",
    "Medical",
    "Stores",
    "Technician",
    "Warden",
]
gender = ["Male", "Female"]
deduction_status = ["Full Deduction", "Partial Deduction", "No Deduction"]
rank = ["Junior", "Senior"]

units_to_add = []
grade_to_add = []
category_to_add = []
deduction_status_to_add = []
gender_to_add = []
rank_to_add = []

with SessionLocal() as db:
    for unit in units:
        value = Unit(name=unit)
        units_to_add.append(value)

    db.add_all(units_to_add)

    for grade in grades:
        value = Grade(name=grade)
        grade_to_add.append(value)

    db.add_all(grade_to_add)

    for category in categories:
        value = Category(name=category)
        category_to_add.append(value)

    db.add_all(category_to_add)

    for name in gender:
        value = Gender(name=name)
        gender_to_add.append(value)

    db.add_all(gender_to_add)

    for name in deduction_status:
        value = DeductionStatus(name=name)
        deduction_status_to_add.append(value)

    db.add_all(deduction_status_to_add)

    for name in rank:
        value = Rank(name=name)
        rank_to_add.append(value)

    db.add_all(rank_to_add)

    db.commit()

print("✅ Database prefilled successfully!")

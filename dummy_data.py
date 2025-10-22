import pandas as pd
from faker import Faker
import random
import os

fake = Faker()

# Number of test rows
n = 6000
ids = random.choices(range(10000, 17000), k=4000)

existing_records = {}
records = []

for _ in range(n):
    service_number = "0" + str(random.choice(ids))

    # Check if this service number already exists
    if service_number in existing_records:
        record = existing_records[service_number].copy()
        # Update only the changing fields
        record["uniform price"] = 2000
        record["amount deducted"] = random.choice([1000, 2000, 500, 1000, 2000])
    else:
        # Generate a new employee record
        record = {
            "service number": service_number,
            "name": fake.first_name(),
            "gender": random.choice(["Male", "Female"]),
            "unit": random.choice(
                ["5 BN", "4 BN", "6 BN", "37 MIL HOSP", "66 ARTY REGT"]
            ),
            "grade": random.choice(
                [
                    "Programmer",
                    "Senior Executive Officer",
                    "Higher Executive Officer",
                    "Executive Officer",
                    "Pharmacist",
                ]
            ),
            "rank": random.choice(["Senior", "Junior"]),
            "category": random.choice(
                [
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
            ),
            "uniform price": 20000,
            "amount deducted": random.choice([200, 100, 300, 400, 50]),
        }
        # Save this record for possible reuse later
        existing_records[service_number] = record.copy()

    records.append(record)

# Convert to DataFrame
df = pd.DataFrame(records)
df.to_excel(
    os.path.join(
        os.path.join(os.path.expanduser("~"), "Desktop"), "test_employees.xlsx"
    ),
    index=False,
)
print("✅ Generated test_employees.xlsx with", len(df), "rows")

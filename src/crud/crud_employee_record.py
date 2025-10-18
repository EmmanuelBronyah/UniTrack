import pandas as pd
from sqlalchemy.orm import Session
from src.database.models import EmployeeRecord, Employee, Occurrence
from decimal import Decimal
from src.utils import (
    missing_headers,
    four_dp_decimal,
    get_date,
    assign_outstanding_amount,
    is_none,
    integrity_error_message,
    validate_field,
    validate_amounts,
    select_value,
    assign_deduction_status,
)
from sqlalchemy.exc import IntegrityError

# TODO: Handle when the Outstanding Difference generates a negative value. This means an employee has been deducted more than the Total Amount to be paid.

# TODO: When data from a file is imported, check service numbers in the data against the service numbers in the database and generate a prompt asking if the existing employee data in the database is to be replaced by the employee data being imported.


def save_from_file(db: Session, file_path: str) -> dict:
    valid_headers = [
        "service number",
        "name",
        "gender",
        "unit",
        "grade",
        "rank",
        "category",
        "uniform price",
        "amount deducted",
    ]
    employee_record_dict = {
        "service_number": "",
        "name": "",
        "gender": "",
        "unit": "",
        "grade": "",
        "rank": "",
        "category": "",
        "uniform_price": "",
        "amount_deducted": "",
        "outstanding_amount": "",
        "deduction_status": "",
    }
    number_of_records_saved = 0
    employee_records_to_save = []
    occurrence_records_to_save = []

    df = pd.read_excel(file_path, dtype=str)

    df = df.fillna("").astype(str)

    headers_in_worksheet = df.columns
    number_of_columns_in_worksheet = len(headers_in_worksheet)
    number_of_headers = len(valid_headers)

    if number_of_columns_in_worksheet == number_of_headers:

        headers_missing_in_worksheet = missing_headers(headers_in_worksheet)

        if headers_missing_in_worksheet:
            return {
                "error": f"Column headers ({', '.join(headers_missing_in_worksheet)}) not found.",
                "records saved": number_of_records_saved,
            }

        else:
            for row_index in range(len(df)):

                employee_record_dict = employee_record_dict.copy()

                for col_index in range(len(df.columns)):

                    header = df.columns[col_index].strip().lower()
                    cell_value = df.iat[row_index, col_index]

                    match header:
                        case "service number" | "name":
                            is_empty = is_none(cell_value)

                            if is_empty:
                                db.rollback()
                                return {
                                    "error": f"{header.capitalize()} must not be empty."
                                }
                            else:
                                result = validate_field(
                                    cell_value,
                                    header,
                                    employee_record_dict,
                                )
                                if not result:
                                    db.rollback()
                                    return {
                                        "error": f"Invalid Service Number: {cell_value} in Service Number column."
                                    }
                                elif result == "EXCEEDED":
                                    return {
                                        "error": f"Invalid Service Number: {cell_value}. Service Number should not exceed seven(7) digits."
                                    }
                                else:
                                    employee_record_dict = result

                        case "gender" | "unit" | "grade" | "rank" | "category":
                            is_empty = is_none(cell_value)

                            if is_empty:
                                db.rollback()
                                return {
                                    "error": f"{header.capitalize()} must not be empty."
                                }
                            else:
                                result = select_value(
                                    cell_value, header, employee_record_dict
                                )
                                if not result:
                                    db.rollback()
                                    return {
                                        "error": f"{header.capitalize()}: {cell_value} does not exist in the database."
                                    }
                                else:
                                    employee_record_dict = result

                        case "uniform price" | "amount deducted":

                            result = validate_amounts(
                                cell_value, header, employee_record_dict
                            )

                            if not result:
                                db.rollback()
                                return {
                                    "error": f"Invalid digits: {cell_value} in {header.capitalize()} column."
                                }
                            else:
                                employee_record_dict = result

                employee_record_dict = assign_outstanding_amount(employee_record_dict)
                result = assign_deduction_status(employee_record_dict)

                if not result:
                    db.rollback()
                    return {
                        "error": "Uniform Price column must not be empty",
                    }

                # Create a new employee if does not exist
                employee = (
                    db.query(Employee)
                    .filter(Employee.service_number == result["service_number"])
                    .first()
                )

                if employee is None:
                    employee = Employee(
                        service_number=result["service_number"],
                        name=result["name"],
                        gender_id=result["gender"],
                        unit_id=result["unit"],
                        grade_id=result["grade"],
                        rank_id=result["rank"],
                        category_id=result["category"],
                    )
                    db.add(employee)
                    db.flush()  # writes to DB, assigns ID, but doesn’t commit yet

                # Get created employee id and assign it to employee's occurrence record
                occurrence = Occurrence(
                    employee_id=employee.id,
                    uniform_price=result["uniform_price"],
                    amount_deducted=result["amount_deducted"],
                    outstanding_amount=result["outstanding_amount"],
                    deduction_status_id=result["deduction_status"],
                )
                db.add(occurrence)

                number_of_records_saved += 1

            db.commit()

            return {"records saved": number_of_records_saved}

    else:
        return {
            "error": "There should be eight (8) columns.",
            "records saved": number_of_records_saved,
        }


def retrieve_records(db: Session) -> list:
    results = db.query(EmployeeRecord).all()
    return results


def retrieve_employee_record(db: Session, service_number) -> EmployeeRecord | dict:
    result = (
        db.query(EmployeeRecord)
        .filter(EmployeeRecord.service_number == service_number)
        .first()
    )

    if result:
        return result
    return {
        "error": f"Employee record with Service Number: {service_number} does not exist."
    }


def save_record(db: Session, employee_record: dict):
    employee_record_dict = {
        "service_number": "",
        "name": "",
        "unit": "",
        "grade": "",
        "appointment_date": "",
        "total_amount": "",
        "amount_deducted": "",
        "outstanding_difference": "",
        "full_payment": False,
        "no_payment": False,
    }
    for key, value in employee_record.items():
        key = key.replace("_", " ")
        match key:
            case "service number" | "name" | "grade" | "unit":
                is_empty = is_none(value)

                if is_empty:
                    return {
                        "error": f"{key.capitalize()} must not be empty.",
                    }
                else:
                    result = validate_field(
                        value,
                        key,
                        employee_record_dict,
                    )
                    if not result:
                        return {
                            "error": f"Invalid Service Number ({value}) in Service Number column.",
                        }
                    else:
                        employee_record_dict = result

            case "appointment date":
                if value:
                    date = get_date(value)

                    if not date:
                        return {
                            "error": f"Invalid date format ({value}). Date should be in the format 'YYYY-MM-DD'.",
                        }

                    employee_record_dict[key.replace(" ", "_")] = date

                else:
                    employee_record_dict[key.replace(" ", "_")] = None

            case "total amount" | "amount deducted" | "outstanding difference":
                result = validate_amounts(value, key, employee_record_dict)

                if not result:
                    return {
                        "error": f"Invalid digits ({value}) in {key.capitalize()} column.",
                    }
                else:
                    employee_record_dict = result

    # employee_record_dict = check_for_no_deductions(employee_record_dict)
    # employee_record_dict = check_for_full_payment(employee_record_dict)

    employee_record_data = EmployeeRecord(**employee_record_dict)

    employee_id = employee_record.get("id", None)
    record = db.query(EmployeeRecord).filter_by(id=employee_id).first()

    if record:
        record.service_number = employee_record_data.service_number
        record.name = employee_record_data.name
        record.unit = employee_record_data.unit
        record.grade = employee_record_data.grade
        record.appointment_date = employee_record_data.appointment_date
        record.total_amount = employee_record_data.total_amount
        record.amount_deducted = employee_record_data.amount_deducted
        record.outstanding_difference = employee_record_data.outstanding_difference
        record.full_payment = employee_record_data.full_payment
        record.no_payment = employee_record_data.no_payment

        db.commit()
        db.refresh(record)

        return record

    return {"error": "Employee record does not exist."}

import pandas as pd
from sqlalchemy.orm import Session
from src.database.models import EmployeeRecord
from decimal import Decimal
from src.utils import (
    missing_headers,
    four_dp_decimal,
    get_date,
    calculate_outstanding_difference,
    check_for_full_payment,
    check_for_no_deductions,
    is_none,
    integrity_error_message,
    validate_field,
    validate_amounts,
)
from sqlalchemy.exc import IntegrityError

# TODO: Handle when the Outstanding Difference generates a negative value. This means an employee has been deducted more than the Total Amount to be paid.

# TODO: When data from a file is imported, check service numbers in the data against the service numbers in the database and generate a prompt asking if the existing employee data in the database is to be replaced by the employee data being imported.


def save_from_file(db: Session, file_path: str) -> dict:
    valid_headers = [
        "service number",
        "name",
        "grade",
        "unit",
        "appointment date",
        "total amount",
        "amount deducted",
        "outstanding difference",
    ]
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
    number_of_records_saved = 0
    records_to_save = []

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

                for col_index in range(len(df.columns)):

                    header = df.columns[col_index].strip().lower()
                    cell_value = df.iat[row_index, col_index]

                    match header:
                        case "service number" | "name" | "grade" | "unit":
                            is_empty = is_none(cell_value)

                            if is_empty:
                                return {
                                    "error": f"{header.capitalize()} must not be empty.",
                                    "records saved": number_of_records_saved,
                                }
                            else:
                                result = validate_field(
                                    cell_value,
                                    header,
                                    employee_record_dict,
                                )
                                if not result:
                                    return {
                                        "error": f"Invalid Service Number ({cell_value}) in Service Number column.",
                                        "records saved": number_of_records_saved,
                                    }
                                else:
                                    employee_record_dict = result

                        case "appointment date":

                            if cell_value:
                                date = get_date(cell_value)

                                if not date:
                                    return {
                                        "error": f"Invalid date format ({cell_value}). Date should be in the format 'YYYY-MM-DD'.",
                                        "records saved": number_of_records_saved,
                                    }

                                employee_record_dict[header.replace(" ", "_")] = date

                            else:
                                employee_record_dict[header.replace(" ", "_")] = None

                        case (
                            "total amount"
                            | "amount deducted"
                            | "outstanding difference"
                        ):

                            result = validate_amounts(
                                cell_value, header, employee_record_dict
                            )

                            if not result:
                                return {
                                    "error": f"Invalid digits ({cell_value}) in {header.capitalize()} column.",
                                    "records saved": number_of_records_saved,
                                }
                            else:
                                employee_record_dict = result

                employee_record_dict = check_for_no_deductions(employee_record_dict)
                employee_record_dict = check_for_full_payment(employee_record_dict)

                employee_record = EmployeeRecord(**employee_record_dict)
                records_to_save.append(employee_record)

                number_of_records_saved += 1

            try:
                db.add_all(records_to_save)
                db.commit()

            except IntegrityError as e:
                db.rollback()

                exception_message = str(e.orig)
                service_number = e.params[0]

                error_message = integrity_error_message(
                    exception_message, service_number
                )

                return {"error": error_message}

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

    employee_record_dict = check_for_no_deductions(employee_record_dict)
    employee_record_dict = check_for_full_payment(employee_record_dict)

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

import pandas as pd
from sqlalchemy.orm import Session
from src.database.models import Employee, Occurrence
from src.utils import (
    missing_headers,
    assign_outstanding_amount,
    is_none,
    validate_field,
    validate_amounts,
    select_value,
    assign_deduction_status,
    same_uniform_price,
    update_outstanding_amount,
    update_deduction_status,
    get_total_amount_deducted,
    get_updated_total_amount_deducted,
)
from sqlalchemy.exc import OperationalError
from sqlalchemy import func


def save_from_file(db: Session, file_path: str, progress_callback=None) -> dict:
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

            try:

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

                    employee_record_dict = assign_outstanding_amount(
                        employee_record_dict, db
                    )
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
                    db.flush()

                    response = same_uniform_price(db, employee.id)
                    if response is not True:
                        db.rollback()
                        return {
                            "error": f"Uniform price mismatch {str(response[0]),  str(response[1])}. Employee Service Number ({response[2]})."
                        }

                    # Assign Total Amount Deducted
                    total_amount_deducted = get_total_amount_deducted(db, employee.id)
                    employee.total_amount_deducted = total_amount_deducted

                    percent = (row_index + 1) / len(df) * 100
                    progress_callback.emit(percent)

                    number_of_records_saved += 1

                db.commit()

                return {"records saved": number_of_records_saved}

            except OperationalError as e:
                if "database is locked" in str(e):
                    return {
                        "error": "Please wait a moment and try again - database busy."
                    }

    else:
        return {
            "error": "There should be eight (8) columns.",
            "records saved": number_of_records_saved,
        }


def retrieve_random_records(db: Session) -> list:
    results = db.query(Employee).order_by(func.random()).limit(10).all()

    if not results:
        return None

    for record in results:
        unit = record.unit.name
        grade = record.grade.name

        setattr(record, "unit_name", unit)
        setattr(record, "grade_name", grade)

    return results


def retrieve_employee_record(db: Session, service_number) -> dict:
    employee_data = {}

    employee = (
        db.query(Employee).filter(Employee.service_number == service_number).first()
    )
    if employee:
        unit = employee.unit.name
        setattr(employee, "unit_name", unit)
        rank = employee.rank.name
        setattr(employee, "rank_name", rank)
        gender = employee.gender.name
        setattr(employee, "gender_name", gender)
        grade = employee.grade.name
        setattr(employee, "grade_name", grade)
        category = employee.category.name
        setattr(employee, "category_name", category)

        employee_data["occurrences"] = [
            setattr(
                occurrence, "deduction_status_name", occurrence.deduction_status.name
            )
            for occurrence in employee.occurrences
        ]
        employee_data["employee"] = employee.__dict__
        employee_data["occurrences"] = [
            occurrence.__dict__ for occurrence in employee.occurrences
        ]

        return employee_data

    return {
        "error": f"Employee record with Service Number: {service_number} does not exist."
    }


def save_record(db: Session, employee_record: dict) -> dict:
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
    for key, value in employee_record.items():
        key = key.replace("_", " ")
        match key:
            case "service number" | "name":
                is_empty = is_none(value)

                if is_empty:
                    db.rollback()
                    return {"error": f"{key.capitalize()} must not be empty."}
                else:
                    result = validate_field(
                        value,
                        key,
                        employee_record_dict,
                    )
                    if not result:
                        db.rollback()
                        return {
                            "error": f"Invalid Service Number: {value} in Service Number column."
                        }
                    elif result == "EXCEEDED":
                        return {
                            "error": f"Invalid Service Number: {value}. Service Number should not exceed seven(7) digits."
                        }
                    else:
                        employee_record_dict = result

            case "gender" | "unit" | "grade" | "rank" | "category":
                is_empty = is_none(value)

                if is_empty:
                    db.rollback()
                    return {"error": f"{key.capitalize()} must not be empty."}
                else:
                    result = select_value(value, key, employee_record_dict)
                    if not result:
                        db.rollback()
                        return {
                            "error": f"{key.capitalize()}: {value} does not exist in the database."
                        }
                    else:
                        employee_record_dict = result

            case "uniform price" | "amount deducted":

                result = validate_amounts(value, key, employee_record_dict)

                if not result:
                    db.rollback()
                    return {
                        "error": f"Invalid digits: {value} in {key.capitalize()} column."
                    }
                else:
                    employee_record_dict = result

    employee_id = employee_record.get("employee_id")
    occurrence_id = employee_record.get("occurrence_id")

    employee_record_dict = update_outstanding_amount(
        employee_record_dict, db, occurrence_id, employee_id
    )

    result = update_deduction_status(db, occurrence_id, employee_record_dict)

    if not result:
        db.rollback()
        return {
            "error": "Uniform Price column must not be empty",
        }

    employee_id = employee_record.get("employee_id")
    record = db.query(Employee).filter(Employee.id == employee_id).first()

    record.service_number = result["service_number"]
    record.name = result["name"]
    record.gender_id = result["gender"]
    record.unit_id = result["unit"]
    record.grade_id = result["grade"]
    record.category_id = result["category"]
    record.rank_id = result["rank"]

    current_amount_deducted = employee_record_dict.get("amount_deducted")
    total_amount_deducted = get_updated_total_amount_deducted(
        db, employee_id, occurrence_id, current_amount_deducted
    )

    record.total_amount_deducted = total_amount_deducted

    db.commit()
    db.refresh(record)

    employee = retrieve_employee_record(db, record.service_number)
    return employee


def delete_record(db: Session, occurrence_id: int, employee_id: int) -> str | bool:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    occurrence = db.query(Occurrence).filter(Occurrence.id == occurrence_id).first()
    all_occurrences = (
        db.query(Occurrence).filter(Occurrence.employee_id == employee_id).all()
    )

    number_of_occurrences = len(all_occurrences)

    if number_of_occurrences == 1:

        if occurrence:

            db.delete(occurrence)
            db.delete(employee)

            db.commit()

            return "DELETED LAST OCCURRENCE AND ASSOCIATED EMPLOYEE"
    else:

        if occurrence:

            db.delete(occurrence)
            db.commit()

            return True


def add_record(db: Session, record: dict) -> dict | bool:
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
    for key, value in record.items():
        key = key.replace("_", " ")

        match key:
            case "service number" | "name":
                is_empty = is_none(value)

                if is_empty:
                    db.rollback()
                    return {"error": f"{key.capitalize()} must not be empty."}
                else:
                    result = validate_field(
                        value,
                        key,
                        employee_record_dict,
                    )
                    if not result:
                        db.rollback()
                        return {
                            "error": f"Invalid Service Number: {value} in Service Number column."
                        }
                    elif result == "EXCEEDED":
                        return {
                            "error": f"Invalid Service Number: {value}. Service Number should not exceed seven(7) digits."
                        }
                    else:
                        employee_record_dict = result

            case "gender" | "unit" | "grade" | "rank" | "category":
                is_empty = is_none(value)

                if is_empty:
                    db.rollback()
                    return {"error": f"{key.capitalize()} must not be empty."}
                else:
                    result = select_value(value, key, employee_record_dict)
                    if not result:
                        db.rollback()
                        return {
                            "error": f"{key.capitalize()}: {value} does not exist in the database."
                        }
                    else:
                        employee_record_dict = result

            case "uniform price" | "amount deducted":

                result = validate_amounts(value, key, employee_record_dict)

                if not result:
                    db.rollback()
                    return {
                        "error": f"Invalid digits: {value} in {key.capitalize()} column."
                    }
                else:
                    employee_record_dict = result

    employee_record_dict = assign_outstanding_amount(employee_record_dict, db)
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
    db.flush()

    response = same_uniform_price(db, employee.id)
    if response is not True:
        db.rollback()
        return {
            "error": f"Uniform price mismatch {str(response[0]),  str(response[1])}. Employee Service Number ({response[2]})."
        }

    # Assign Total Amount Deducted
    total_amount_deducted = get_total_amount_deducted(db, employee.id)
    employee.total_amount_deducted = total_amount_deducted

    db.commit()

    return True


def search_record(db: Session, service_number=None, name=None):
    search_by_service_number = (Employee.service_number).like(f"%{service_number}%")
    search_by_name = func.lower(Employee.name).like(f"%{name.lower()}%")

    if service_number:
        results = db.query(Employee).filter(search_by_service_number).all()

        if results:

            for record in results:
                unit = record.unit.name
                setattr(record, "unit_name", unit)
                rank = record.rank.name
                setattr(record, "rank_name", rank)
                gender = record.gender.name
                setattr(record, "gender_name", gender)
                grade = record.grade.name
                setattr(record, "grade_name", grade)
                category = record.category.name
                setattr(record, "category_name", category)

        return results

    elif name:
        results = db.query(Employee).filter(search_by_name).all()

        if results:

            for record in results:
                unit = record.unit.name
                setattr(record, "unit_name", unit)
                rank = record.rank.name
                setattr(record, "rank_name", rank)
                gender = record.gender.name
                setattr(record, "gender_name", gender)
                grade = record.grade.name
                setattr(record, "grade_name", grade)
                category = record.category.name
                setattr(record, "category_name", category)

        return results

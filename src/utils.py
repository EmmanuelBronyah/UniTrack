from PySide6 import QtWidgets, QtGui, QtCore
from src.components.loginscreen import LoginScreen
import resources
from decimal import Decimal, ROUND_HALF_UP
from decimal import InvalidOperation
from datetime import datetime
from src.database.db import SessionLocal
from src.database.models import (
    Gender,
    Grade,
    Rank,
    Category,
    Unit,
    DeductionStatus,
    Employee,
    Occurrence,
)
from sqlalchemy import func
import pandas as pd


def load_fonts():
    lato_font_path = ":/assets/fonts/lato"
    oswald_font_path_bold = ":/assets/fonts/oswald_bold"

    QtGui.QFontDatabase.addApplicationFont(lato_font_path)
    QtGui.QFontDatabase.addApplicationFont(oswald_font_path_bold)


def load_styles(app):

    load_fonts()
    app.setFont("Lato")

    file = QtCore.QFile(":/assets/styles/style")
    if file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
        stream = QtCore.QTextStream(file)
        app.setStyleSheet(stream.readAll())
        file.close()


_animations = []


def show_screen(screen, func):
    opacity_effect = QtWidgets.QGraphicsOpacityEffect(screen)
    screen.setGraphicsEffect(opacity_effect)
    fade_out = QtCore.QPropertyAnimation(opacity_effect, b"opacity")
    fade_out.setDuration(1000)
    fade_out.setStartValue(1)
    fade_out.setEndValue(0)
    fade_out.finished.connect(func)
    _animations.append(fade_out)
    fade_out.start()


def fade_in_screen(stacked_widget, screen):
    if isinstance(screen, LoginScreen):
        stacked_widget.setCurrentIndex(1)
    else:
        stacked_widget.setCurrentIndex(2)
    opacity_effect = QtWidgets.QGraphicsOpacityEffect(screen)
    screen.setGraphicsEffect(opacity_effect)
    fade_in = QtCore.QPropertyAnimation(opacity_effect, b"opacity")
    fade_in.setDuration(1000)
    fade_in.setStartValue(0)
    fade_in.setEndValue(1)
    _animations.append(fade_in)
    fade_in.start()


def missing_headers(headers_in_worksheet):
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

    headers_found_in_worksheet = []

    for header in headers_in_worksheet:
        if header.lower() in valid_headers:
            headers_found_in_worksheet.append(header)

    headers_found_in_worksheet = [
        header.lower() for header in headers_found_in_worksheet
    ]

    headers_missing_in_worksheet = list(
        set(valid_headers) - set(headers_found_in_worksheet)
    )

    return headers_missing_in_worksheet


def two_dp_decimal(cell_value):
    try:
        return Decimal(str(cell_value)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    except InvalidOperation:
        return None


def get_date(cell_value):
    try:
        return datetime.strptime(cell_value, "%Y-%m-%d %H:%M:%S").date()
    except ValueError:
        try:
            return datetime.strptime(cell_value, "%Y-%m-%d").date()
        except ValueError:
            return False


def assign_outstanding_amount(employee_record_dict, db):
    service_number = employee_record_dict["service_number"]

    uniform_price = employee_record_dict["uniform_price"]
    uniform_price = two_dp_decimal(uniform_price)

    current_amount_deducted = employee_record_dict["amount_deducted"]
    current_amount_deducted = two_dp_decimal(current_amount_deducted)

    cumulated_deduction = Decimal("0.00")

    employee = (
        db.query(Employee).filter(Employee.service_number == service_number).first()
    )

    if employee:

        employee_id = employee.id

        occurrences = (
            db.query(Occurrence).filter(Occurrence.employee_id == employee_id).all()
        )

        if occurrences:

            for occurrence in occurrences:
                amount_deducted = occurrence.amount_deducted
                amount_deducted = two_dp_decimal(amount_deducted)

                cumulated_deduction += amount_deducted
                cumulated_deduction = two_dp_decimal(cumulated_deduction)

            cumulated_deduction = cumulated_deduction + current_amount_deducted
            cumulated_deduction = two_dp_decimal(cumulated_deduction)

            difference = uniform_price - cumulated_deduction
            difference = two_dp_decimal(difference)

            employee_record_dict["outstanding_amount"] = difference

            return employee_record_dict

    difference = uniform_price - current_amount_deducted
    difference = two_dp_decimal(difference)

    employee_record_dict["outstanding_amount"] = difference

    return employee_record_dict


def assign_deduction_status(employee_record_dict):
    with SessionLocal() as db:
        uniform_price = employee_record_dict["uniform_price"]
        uniform_price = two_dp_decimal(uniform_price)

        amount_deducted = employee_record_dict["amount_deducted"]
        amount_deducted = two_dp_decimal(amount_deducted)

        difference = uniform_price - amount_deducted
        difference = two_dp_decimal(difference)

        if not uniform_price.is_zero():

            if amount_deducted.is_zero():
                value_id = (
                    db.query(DeductionStatus)
                    .filter(func.lower(DeductionStatus.name) == "no deduction")
                    .first()
                    .id
                )
                employee_record_dict["deduction_status"] = value_id

                return employee_record_dict

            elif difference.is_zero():
                value_id = (
                    db.query(DeductionStatus)
                    .filter(func.lower(DeductionStatus.name) == "full deduction")
                    .first()
                    .id
                )
                employee_record_dict["deduction_status"] = value_id

                return employee_record_dict

            elif not difference.is_zero() and not difference.is_signed():
                value_id = (
                    db.query(DeductionStatus)
                    .filter(func.lower(DeductionStatus.name) == "partial deduction")
                    .first()
                    .id
                )
                employee_record_dict["deduction_status"] = value_id

                return employee_record_dict

            elif not difference.is_zero() and difference.is_signed():
                value_id = (
                    db.query(DeductionStatus)
                    .filter(func.lower(DeductionStatus.name) == "full deduction")
                    .first()
                    .id
                )
                employee_record_dict["deduction_status"] = value_id

                return employee_record_dict

        else:
            return False


def update_deduction_status(db, occurrence_id, employee_record_dict):
    occurrence = db.query(Occurrence).filter(Occurrence.id == occurrence_id).first()

    uniform_price = occurrence.uniform_price
    uniform_price = two_dp_decimal(uniform_price)

    amount_deducted = occurrence.amount_deducted
    amount_deducted = two_dp_decimal(amount_deducted)

    difference = uniform_price - amount_deducted
    difference = two_dp_decimal(difference)

    if not uniform_price.is_zero():

        if amount_deducted.is_zero():
            value_id = (
                db.query(DeductionStatus)
                .filter(func.lower(DeductionStatus.name) == "no deduction")
                .first()
                .id
            )
            occurrence.deduction_status_id = value_id
            employee_record_dict["deduction_status"] = value_id

            return employee_record_dict

        elif difference.is_zero():
            value_id = (
                db.query(DeductionStatus)
                .filter(func.lower(DeductionStatus.name) == "full deduction")
                .first()
                .id
            )
            occurrence.deduction_status_id = value_id
            employee_record_dict["deduction_status"] = value_id

            return employee_record_dict

        elif not difference.is_zero() and not difference.is_signed():
            value_id = (
                db.query(DeductionStatus)
                .filter(func.lower(DeductionStatus.name) == "partial deduction")
                .first()
                .id
            )
            occurrence.deduction_status_id = value_id
            employee_record_dict["deduction_status"] = value_id

            return employee_record_dict

        elif not difference.is_zero() and difference.is_signed():
            value_id = (
                db.query(DeductionStatus)
                .filter(func.lower(DeductionStatus.name) == "full deduction")
                .first()
                .id
            )
            occurrence.deduction_status_id = value_id
            employee_record_dict["deduction_status"] = value_id

            return employee_record_dict


def is_none(cell_value):
    return True if not cell_value else False


def validate_field(cell_value, header, employee_record_dict):
    if header == "service number":

        if cell_value.isdigit():
            max_service_number_length = 7
            service_number_length = len(list(cell_value))

            if service_number_length > max_service_number_length:
                return "EXCEEDED"

            employee_record_dict[header.replace(" ", "_")] = cell_value
            return employee_record_dict
        else:
            return False
    else:
        employee_record_dict[header] = cell_value
        return employee_record_dict


def validate_amounts(cell_value, header, employee_record_dict):
    if cell_value:
        amount = two_dp_decimal(cell_value)

        if amount is None:
            return False

        employee_record_dict[header.replace(" ", "_")] = amount
        return employee_record_dict


def select_value(cell_value, header, employee_record_dict):
    with SessionLocal() as db:
        if header.lower() == "gender":
            value = (
                db.query(Gender)
                .filter(func.lower(Gender.name) == cell_value.strip().lower())
                .first()
            )
            if value:
                employee_record_dict["gender"] = value.id
                return employee_record_dict
            return False

        elif header.lower() == "unit":
            value = (
                db.query(Unit)
                .filter(func.lower(Unit.name) == cell_value.strip().lower())
                .first()
            )
            if value:
                employee_record_dict["unit"] = value.id
                return employee_record_dict
            return False

        elif header.lower() == "grade":
            value = (
                db.query(Grade)
                .filter(func.lower(Grade.name) == cell_value.strip().lower())
                .first()
            )
            if value:
                employee_record_dict["grade"] = value.id
                return employee_record_dict
            return False

        elif header.lower() == "rank":
            value = (
                db.query(Rank)
                .filter(func.lower(Rank.name) == cell_value.strip().lower())
                .first()
            )
            if value:
                employee_record_dict["rank"] = value.id
                return employee_record_dict
            return False

        elif header.lower() == "category":
            value = (
                db.query(Category)
                .filter(func.lower(Category.name) == cell_value.strip().lower())
                .first()
            )
            if value:
                employee_record_dict["category"] = value.id
                return employee_record_dict
            return False


def employee_data_info_error(employee_data_info):
    employee_data_info.setStyleSheet(
        """
        background-color: #dc3545;
        color: white;
        font-weight: bold;
        border-radius: 5;
        padding: 3;
        """
    )


def employee_data_info_success(employee_data_info):
    employee_data_info.setStyleSheet(
        """
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border-radius: 5;
        padding: 3;
        """
    )


def employee_data_info_warning(employee_data_info):
    employee_data_info.setStyleSheet(
        """
        background-color: #FFCC00;
        color: white;
        font-weight: bold;
        border-radius: 5;
        padding: 3;
        """
    )


def integrity_error_message(error, service_number):
    if "UNIQUE constraint failed: employee_records.service_number" in error:
        return (
            f"Employee record with Service Number: '{service_number}' already exists."
        )


def deduction_exceeded_warning(deduction_exceeded):
    deduction_exceeded.setStyleSheet(
        """
        background-color: #dc3545;
        color: white;
        font-weight: bold;
        border-radius: 5;
        padding: 3;
        """
    )


RANK = ["Junior", "Senior"]
CATEGORY = [
    "Artisan",
    "Chief Yard Foreman",
    "Driver",
    "Field Worker",
    "General",
    "Labourer",
    "Medical",
    "Supply",
    "Technician",
    "Warden",
]
UNIT = ["5 BN", "4 BN", "6 BN", "37 MIL HOSP", "66 ARTY REGT"]
GENDER = ["Male", "Female"]
DEDUCTION_STATUS = ["Full Deduction", "Partial Deduction", "No Deduction"]
GRADE = [
    "Programmer",
    "Senior Executive Officer",
    "Higher Executive Officer",
    "Executive Officer",
    "Pharmacist",
]
FILTER_EXPORT_CRITERIA = [
    "Full Deduction",
    "Partial Deduction",
    "Exceeded Deduction",
    "No Deduction",
]


def setup_combobox(combobox, role):
    dropdown_data = {
        "rank": RANK,
        "category": CATEGORY,
        "unit": UNIT,
        "gender": GENDER,
        "deduction_status": DEDUCTION_STATUS,
        "grade": GRADE,
        "filter_export_criteria": FILTER_EXPORT_CRITERIA,
    }

    match role:
        case (
            "rank"
            | "category"
            | "unit"
            | "gender"
            | "deduction_status"
            | "grade"
            | "filter_export_criteria"
        ):
            combobox.addItems(dropdown_data[role])
            combobox.setEditable(True)

            completer = QtWidgets.QCompleter(dropdown_data[role])
            completer.setCaseSensitivity(
                QtCore.Qt.CaseSensitivity(False)
            )  # Case-insensitive
            completer.setFilterMode(
                QtCore.Qt.MatchContains
            )  # Match text anywhere, not just start
            combobox.setCompleter(completer)
            return combobox


def calculate_total_amount_deducted(occurrences):
    total_amount_deducted = Decimal("0.00")

    for occurrence in occurrences:
        amount_deducted = occurrence.get("amount_deducted", None)
        amount_deducted = two_dp_decimal(amount_deducted)

        total_amount_deducted += amount_deducted

    total_amount_deducted = two_dp_decimal(total_amount_deducted)

    return total_amount_deducted


def final_occurrence_deduction_status(uniform_price, amount_deducted):
    uniform_price = two_dp_decimal(uniform_price)
    amount_deducted = two_dp_decimal(amount_deducted)

    difference = uniform_price - amount_deducted
    difference = two_dp_decimal(difference)

    if amount_deducted.is_zero():
        return ["No Deduction", difference]

    elif difference.is_zero():
        return ["Full Deduction", difference]

    elif not difference.is_zero() and not difference.is_signed():
        return ["Partial Deduction", difference]

    elif not difference.is_zero() and difference.is_signed():
        return ["Full Deduction", difference]


def same_uniform_price(db, employee_id):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    occurrences = (
        db.query(Occurrence).filter(Occurrence.employee_id == employee_id).all()
    )

    first_uniform_price = occurrences[0].uniform_price
    first_uniform_price = two_dp_decimal(first_uniform_price)

    for occurrence in occurrences:
        uniform_price = occurrence.uniform_price
        uniform_price = two_dp_decimal(uniform_price)

        same_price = first_uniform_price == uniform_price

        if same_price:
            continue
        else:
            return (
                first_uniform_price,
                uniform_price,
                employee.service_number,
            )

    return True


def update_outstanding_amount(employee_record_dict, db, occurrence_id, employee_id):
    uniform_price = employee_record_dict["uniform_price"]
    uniform_price = two_dp_decimal(uniform_price)

    current_amount_deducted = employee_record_dict["amount_deducted"]
    current_amount_deducted = two_dp_decimal(current_amount_deducted)

    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    occurrences = (
        db.query(Occurrence).filter(Occurrence.employee_id == employee_id).all()
    )

    cumulated_deduction = Decimal("0.00")

    if employee and occurrences:
        for occurrence in occurrences:
            occurrence.uniform_price = uniform_price

            if occurrence.id == occurrence_id:
                occurrence.amount_deducted = current_amount_deducted

            cumulated_deduction += occurrence.amount_deducted
            cumulated_deduction = two_dp_decimal(cumulated_deduction)

            difference = uniform_price - cumulated_deduction
            difference = two_dp_decimal(difference)

            occurrence.outstanding_amount = difference

            employee_record_dict["outstanding_amount"] = difference

        return employee_record_dict


def recalculate_outstanding_amount_after_deletion(db, employee_id):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    service_number = employee.service_number

    occurrences = (
        db.query(Occurrence).filter(Occurrence.employee_id == employee_id).all()
    )

    cumulated_deduction = Decimal("0.00")

    if occurrences:

        for occurrence in occurrences:
            amount_deducted = occurrence.amount_deducted

            cumulated_deduction += amount_deducted
            cumulated_deduction = two_dp_decimal(cumulated_deduction)

            outstanding_amount = occurrence.uniform_price - cumulated_deduction
            outstanding_amount = two_dp_decimal(outstanding_amount)
            occurrence.outstanding_amount = outstanding_amount

        db.commit()

    return service_number


def is_exceeded_deduction(db, employee_id):
    occurrences = (
        db.query(Occurrence).filter(Occurrence.employee_id == employee_id).all()
    )

    uniform_price = occurrences[0].uniform_price
    uniform_price = two_dp_decimal(uniform_price)

    cumulated_deduction = Decimal("0.00")

    for occurrence in occurrences:
        amount_deducted = occurrence.amount_deducted

        cumulated_deduction += amount_deducted
        cumulated_deduction = two_dp_decimal(cumulated_deduction)

    outstanding_amount = uniform_price - cumulated_deduction
    outstanding_amount = two_dp_decimal(outstanding_amount)

    if outstanding_amount.is_signed():
        return True

    return False


def get_total_amount_deducted(db, employee_id):
    total_amount_deducted = Decimal("0.00")

    occurrences = (
        db.query(Occurrence).filter(Occurrence.employee_id == employee_id).all()
    )

    for occurrence in occurrences:
        amount_deducted = occurrence.amount_deducted
        amount_deducted = two_dp_decimal(amount_deducted)

        total_amount_deducted += amount_deducted
        total_amount_deducted = two_dp_decimal(total_amount_deducted)

    return total_amount_deducted


def get_updated_total_amount_deducted(
    db, employee_id, occurrence_id, current_amount_deducted
):
    total_amount_deducted = Decimal("0.00")

    occurrences = (
        db.query(Occurrence).filter(Occurrence.employee_id == employee_id).all()
    )

    for occurrence in occurrences:

        if occurrence.id == occurrence_id:
            continue

        amount_deducted = occurrence.amount_deducted
        amount_deducted = two_dp_decimal(amount_deducted)

        total_amount_deducted += amount_deducted
        total_amount_deducted = two_dp_decimal(total_amount_deducted)

    updated_total_amount_deducted = total_amount_deducted + current_amount_deducted
    updated_total_amount_deducted = two_dp_decimal(updated_total_amount_deducted)

    return updated_total_amount_deducted


def get_total_amount_deducted_by_service_number(db, service_number):
    employee = (
        db.query(Employee).filter(Employee.service_number == service_number).first()
    )
    employee_id = employee.id

    occurrences = (
        db.query(Occurrence).filter(Occurrence.employee_id == employee_id).all()
    )

    total_amount_deducted = Decimal("0.00")

    for occurrence in occurrences:
        amount_deducted = occurrence.amount_deducted
        amount_deducted = two_dp_decimal(amount_deducted)

        total_amount_deducted += amount_deducted
        total_amount_deducted = two_dp_decimal(total_amount_deducted)

    return total_amount_deducted


def set_total_amount_deducted_on_employee(db, employee_id, total_amount_deducted):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    employee.total_amount_deducted = two_dp_decimal(total_amount_deducted)
    return True


def perform_export(db, file_name, progress_callback=None):
    try:
        records = []

        employees = db.query(Employee).all()

        if not employees:
            return False

        for index, employee in enumerate(employees):
            record = {}

            record["Service Number"] = employee.service_number
            record["Name"] = employee.name
            record["Gender"] = employee.gender.name
            record["Unit"] = employee.unit.name
            record["Grade"] = employee.grade.name
            record["Rank"] = employee.rank.name
            record["Category"] = employee.category.name
            record["Uniform Price"] = str(employee.occurrences[0].uniform_price)
            record["Amount Deducted"] = str(employee.total_amount_deducted)
            record["Outstanding Amount"] = str(
                two_dp_decimal(record["Uniform Price"])
                - two_dp_decimal(record["Amount Deducted"])
            )

            percent = (index + 1) / len(employees) * 100
            progress_callback.emit(percent)

            records.append(record)

        df = pd.DataFrame(records)
        df.to_excel(file_name, index=False)

        number_of_records_exported = len(records)

        return number_of_records_exported

    except PermissionError:
        return {"error": "File is open. Please close file and try again"}

    except Exception:
        return {"error": "An error occurred. Please try again"}

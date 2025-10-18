from PySide6 import QtWidgets, QtGui, QtCore
from src.components.loginscreen import LoginScreen
import resources
from decimal import Decimal, ROUND_HALF_UP
from decimal import InvalidOperation
from datetime import datetime
from src.database.db import SessionLocal
from src.database.models import Gender, Grade, Rank, Category, Unit, DeductionStatus
from sqlalchemy import func


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


def four_dp_decimal(cell_value):
    try:
        return Decimal(cell_value).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
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


def assign_outstanding_amount(employee_record_dict):
    uniform_price = employee_record_dict["uniform_price"]
    amount_deducted = employee_record_dict["amount_deducted"]

    difference = uniform_price - amount_deducted
    employee_record_dict["outstanding_amount"] = difference

    return employee_record_dict


def assign_deduction_status(employee_record_dict):
    with SessionLocal() as db:
        uniform_price = employee_record_dict["uniform_price"]
        amount_deducted = employee_record_dict["amount_deducted"]
        difference = uniform_price - amount_deducted

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
        amount = four_dp_decimal(cell_value)

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

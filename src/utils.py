from PySide6 import QtWidgets, QtGui, QtCore
from src.components.loginscreen import LoginScreen
import resources
from decimal import Decimal, ROUND_HALF_UP
from decimal import InvalidOperation
from datetime import datetime


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
        "grade",
        "unit",
        "appointment date",
        "total amount",
        "amount deducted",
        "outstanding difference",
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


def calculate_outstanding_difference(total_amount, amount_deducted):
    return total_amount - amount_deducted


def check_for_no_deductions(employee_record_dict):
    amount_deducted = employee_record_dict["amount_deducted"]
    if amount_deducted.is_zero():
        employee_record_dict["no_payment"] = True
        return employee_record_dict

    else:
        employee_record_dict["no_payment"] = False
        return employee_record_dict


def check_for_full_payment(employee_record_dict):
    total_amount = employee_record_dict["total_amount"]
    amount_deducted = employee_record_dict["amount_deducted"]
    difference = total_amount - amount_deducted

    if total_amount.is_zero() and amount_deducted.is_zero():
        employee_record_dict["full_payment"] = False
        return employee_record_dict

    elif difference.is_zero():
        employee_record_dict["full_payment"] = True
        return employee_record_dict

    elif not difference.is_zero() and not difference.is_signed():
        employee_record_dict["full_payment"] = False
        return employee_record_dict

    elif not difference.is_zero() and difference.is_signed():
        employee_record_dict["full_payment"] = True
        return employee_record_dict


def is_none(cell_value):
    return True if not cell_value else False


def validate_field(cell_value, header, employee_record_dict):
    if header == "service number":
        if cell_value.isdigit():
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

    else:
        if header == "outstanding difference":
            amount = calculate_outstanding_difference(
                employee_record_dict["total_amount"],
                employee_record_dict["amount_deducted"],
            )
            employee_record_dict[header.replace(" ", "_")] = amount
            return employee_record_dict
        else:
            employee_record_dict[header.replace(" ", "_")] = Decimal("0.0000")
            return employee_record_dict


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

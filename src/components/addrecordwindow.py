from PySide6 import QtWidgets, QtCore, QtGui
from src.utils import (
    deduction_exceeded_warning,
    employee_data_info_error,
    employee_data_info_success,
)
import traceback
from src.crud.crud_employee_record import save_record
from src.database.db import SessionLocal
import sys


class AddRecordWindow(QtWidgets.QMainWindow):
    def __init__(self, employee_data):
        super().__init__()

        self.employee_data = employee_data

        self.setup_window()
        self.setup_container()
        self.setup_form_widgets()
        self.setup_buttons()
        self.setup_footer()
        self.check_exceeded_deduction()

    def setup_window(self):
        self.setFixedSize(QtCore.QSize(800, 400))
        self.setWindowIcon(QtGui.QIcon(":/assets/icons/unitrack_icon"))
        self.setStyleSheet(
            """
            background-color: #DBDBDB;
            font-weight: bold;
            color: #3B3B3B;
            """
        )
        self.setWindowTitle("Employee Record Info")

    def setup_container(self):
        self.container_widget = QtWidgets.QWidget()
        self.container_widget.setContentsMargins(10, 5, 10, 5)

        self.container_layout = QtWidgets.QVBoxLayout(self.container_widget)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(10)

        self.setCentralWidget(self.container_widget)

    def setup_form_widgets(self):
        self.form_widget = QtWidgets.QWidget()
        self.form_widget.setContentsMargins(0, 0, 0, 0)

        self.form_layout = QtWidgets.QGridLayout(self.form_widget)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(6)

        self.service_number = self.employee_data["service_number"]
        self.service_number_label = QtWidgets.QLabel("Service Number")
        self.service_number_input = QtWidgets.QLineEdit(text=self.service_number)
        self.service_number_input.setFixedHeight(35)
        self.service_number_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.form_layout.addWidget(self.service_number_label, 0, 0)
        self.form_layout.addWidget(self.service_number_input, 1, 0)

        self.name = self.employee_data["name"]
        self.name_label = QtWidgets.QLabel("Name")
        self.name_input = QtWidgets.QLineEdit(text=self.name)
        self.name_input.setFixedHeight(35)
        self.name_input.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.form_layout.addWidget(self.name_label, 0, 1)
        self.form_layout.addWidget(self.name_input, 1, 1)

        self.unit = self.employee_data["unit"]
        self.unit_label = QtWidgets.QLabel("Unit")
        self.unit_input = QtWidgets.QLineEdit(text=self.unit)
        self.unit_input.setFixedHeight(35)
        self.unit_input.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.form_layout.addWidget(self.unit_label, 0, 2)
        self.form_layout.addWidget(self.unit_input, 1, 2)

        self.grade = self.employee_data["grade"]
        self.grade_label = QtWidgets.QLabel("Grade")
        self.grade_input = QtWidgets.QLineEdit(text=self.grade)
        self.grade_input.setFixedHeight(35)
        self.grade_input.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.form_layout.addWidget(self.grade_label, 2, 0)
        self.form_layout.addWidget(self.grade_input, 3, 0)

        self.appointment_date = self.employee_data["appointment_date"]
        self.appointment_date_label = QtWidgets.QLabel("Appointment Date")
        self.appointment_date_input = QtWidgets.QDateEdit(date=self.appointment_date)
        self.appointment_date_input.setDisplayFormat("yyyy-MM-dd")
        self.appointment_date_input.setCalendarPopup(True)
        self.appointment_date_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.form_layout.addWidget(self.appointment_date_label, 2, 1)
        self.form_layout.addWidget(self.appointment_date_input, 3, 1)

        self.total_amount = self.employee_data["total_amount"]
        self.total_amount_label = QtWidgets.QLabel("Total Amount")
        self.total_amount_input = QtWidgets.QLineEdit(text=str(self.total_amount))
        self.total_amount_input.setFixedHeight(35)
        self.total_amount_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.form_layout.addWidget(self.total_amount_label, 2, 2)
        self.form_layout.addWidget(self.total_amount_input, 3, 2)

        self.amount_deducted = self.employee_data["amount_deducted"]
        self.amount_deducted_label = QtWidgets.QLabel("Amount Deducted")
        self.amount_deducted_input = QtWidgets.QLineEdit(text=str(self.amount_deducted))
        self.amount_deducted_input.setFixedHeight(35)
        self.amount_deducted_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.form_layout.addWidget(self.amount_deducted_label, 4, 0)
        self.form_layout.addWidget(self.amount_deducted_input, 5, 0)

        self.outstanding_difference = self.employee_data["outstanding_difference"]
        self.outstanding_difference_label = QtWidgets.QLabel("Outstanding Difference")
        self.outstanding_difference_input = QtWidgets.QLineEdit(
            text=str(self.outstanding_difference)
        )
        self.outstanding_difference_input.setFixedHeight(35)
        self.outstanding_difference_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.form_layout.addWidget(self.outstanding_difference_label, 4, 1)
        self.form_layout.addWidget(self.outstanding_difference_input, 5, 1)

        self.full_payment = self.employee_data["full_payment"]
        self.full_payment_label = QtWidgets.QLabel("Full Payment")
        self.full_payment_input = QtWidgets.QCheckBox()
        self.full_payment_input.setChecked(self.full_payment)
        self.full_payment_input.setStyleSheet(
            """
            QCheckBox::indicator:checked {
                background-color: green;
                border-radius: 5;
            }
            QCheckBox::indicator:unchecked {
                background-color: red;
                border-radius: 5;
            }
            """
        )
        self.form_layout.addWidget(self.full_payment_label, 4, 2)
        self.form_layout.addWidget(self.full_payment_input, 5, 2)

        self.created_at = self.employee_data["created_at"]
        self.created_at_label = QtWidgets.QLabel("Created At")
        self.created_at_input = QtWidgets.QLineEdit(
            readOnly=True, text=str(self.created_at)
        )
        self.created_at_input.setFixedHeight(35)
        self.created_at_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.form_layout.addWidget(self.created_at_label, 6, 0)
        self.form_layout.addWidget(self.created_at_input, 7, 0)

        self.updated_at = self.employee_data["updated_at"]
        self.updated_at_label = QtWidgets.QLabel("Updated At")
        self.updated_at_input = QtWidgets.QLineEdit(
            readOnly=True, text=str(self.updated_at)
        )
        self.updated_at_input.setFixedHeight(35)
        self.updated_at_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.form_layout.addWidget(self.updated_at_label, 6, 1)
        self.form_layout.addWidget(self.updated_at_input, 7, 1)

        self.no_payment = self.employee_data["no_payment"]
        self.no_payment_label = QtWidgets.QLabel("No Payment")
        self.no_payment_input = QtWidgets.QCheckBox()
        self.no_payment_input.setChecked(self.no_payment)
        self.no_payment_input.setStyleSheet(
            """
            QCheckBox::indicator:checked {
                background-color: green;
                border-radius: 5;
            }
            QCheckBox::indicator:unchecked {
                background-color: red;
                border-radius: 5;
            }
            """
        )
        self.form_layout.addWidget(self.no_payment_label, 6, 2)
        self.form_layout.addWidget(self.no_payment_input, 7, 2)

        self.container_layout.addWidget(self.form_widget, stretch=4)

    def setup_buttons(self):
        self.buttons_widget = QtWidgets.QWidget()
        self.buttons_widget.setContentsMargins(0, 0, 0, 0)

        self.buttons_layout = QtWidgets.QHBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(0)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setFixedHeight(40)
        self.save_button.setFixedWidth(120)
        self.save_button.setStyleSheet(
            """
                background-color: #8B4513;
                color: white;
                font-weight: bold;
                border-radius: 5;
            """
        )
        self.save_button.clicked.connect(self.save_record)
        self.buttons_layout.addWidget(self.save_button)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setFixedHeight(40)
        self.cancel_button.setFixedWidth(120)
        self.cancel_button.setStyleSheet(
            """
                background-color: #8B4513;
                color: white;
                font-weight: bold;
                border-radius: 5;
            """
        )
        self.buttons_layout.addWidget(self.cancel_button)

        self.container_layout.addWidget(self.buttons_widget, stretch=1)

    def setup_footer(self):
        self.footer_widget = QtWidgets.QWidget()
        self.footer_widget.setContentsMargins(0, 0, 0, 0)

        self.footer_layout = QtWidgets.QHBoxLayout(self.footer_widget)
        self.footer_layout.setContentsMargins(0, 0, 0, 0)

        self.employee_record_info = QtWidgets.QLabel()
        self.employee_record_info.setWordWrap(True)
        self.employee_record_info.setVisible(True)
        self.employee_record_info.setStyleSheet(
            """
            background-color: #DBDBDB;
            color: #DBDBDB;
            font-weight: bold; 
            border-radius: 5; 
            padding: 3;
            """
        )

        self.loading_indicator_box = QtWidgets.QLabel()
        self.loading_indicator_box.setFixedSize(45, 45)
        self.loading_indicator_box.setVisible(False)

        self.loading_indicator = QtGui.QMovie(":/assets/icons/spinner-gif")
        self.loading_indicator.setScaledSize(self.loading_indicator_box.size())
        self.loading_indicator_box.setMovie(self.loading_indicator)

        self.product_version_info = QtWidgets.QLabel("UniTrack v1.0.0")
        self.product_version_info.setStyleSheet("color: #8c8c8c; font-weight: bold;")

        self.footer_layout.addWidget(
            self.employee_record_info,
            alignment=QtCore.Qt.AlignmentFlag.AlignLeft,
            stretch=1,
        )
        self.footer_layout.addWidget(
            self.loading_indicator_box,
            alignment=QtCore.Qt.AlignmentFlag.AlignVCenter,
            stretch=1,
        )
        self.footer_layout.addWidget(
            self.product_version_info,
            alignment=QtCore.Qt.AlignmentFlag.AlignRight,
            stretch=1,
        )

        self.container_layout.addWidget(self.footer_widget, stretch=1)

    def check_exceeded_deduction(self):
        if self.outstanding_difference.is_signed():
            self.employee_record_info.setText("Deduction Exceeded")
            self.employee_record_info.setVisible(True)
            deduction_exceeded_warning(self.employee_record_info)

    def handle_error(self, error_tuple): ...

    def display_updated_values(self, response):
        self.loading_indicator.stop()
        self.loading_indicator_box.setVisible(False)

        if isinstance(response, dict):
            if "error" in response:
                error = response.get("error")
                self.employee_record_info.setText(error)
                employee_data_info_error(self.employee_record_info)
        else:
            self.employee_record_info.setText("Record Updated")
            employee_data_info_success(self.employee_record_info)

            # TODO: Display Values

    def update_data(self, updated_employee_data):
        with SessionLocal() as db:
            result = save_record(db, updated_employee_data)
            return result

    def save_record(self):
        self.loading_indicator_box.setVisible(True)
        self.loading_indicator.start()

        self.updated_employee_data = {
            "id": self.employee_data.get("id", None),
            "service_number": self.service_number_input.text(),
            "name": self.name_input.text(),
            "unit": self.unit_input.text(),
            "grade": self.grade_input.text(),
            "appointment_date": self.appointment_date_input.text(),
            "total_amount": self.total_amount_input.text(),
            "amount_deducted": self.amount_deducted_input.text(),
            "outstanding_difference": self.outstanding_difference_input.text(),
            "full_payment": self.full_payment_input.isChecked(),
            "no_payment": self.no_payment_input.isChecked(),
        }

        self.save_record_threadpool = QtCore.QThreadPool()
        self.save_record_worker = Worker(self.update_data, self.updated_employee_data)
        self.save_record_worker.signals.result.connect(self.display_updated_values)
        self.save_record_worker.signals.error.connect(self.handle_error)
        self.save_record_threadpool.start(self.save_record_worker)


class WorkerSignals(QtCore.QObject):

    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)
    progress = QtCore.Signal(float)


class Worker(QtCore.QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super().__init__(self)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.progress_callback = self.signals.progress

    @QtCore.Slot()
    def run(self):

        try:
            result = self.fn(*self.args, **self.kwargs)

        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))

        else:
            self.signals.result.emit(result)

        finally:
            self.signals.finished.emit()

from PySide6 import QtWidgets, QtCore, QtGui
import resources
from src.utils import (
    setup_combobox,
    employee_data_info_error,
    employee_data_info_success,
    calculate_total_amount_deducted,
    get_total_amount_deducted_by_service_number,
    two_dp_decimal,
)
from src.components.workerclass import Worker
from src.database.db import SessionLocal
from src.crud.crud_employee_record import retrieve_employee_record, add_record
from decimal import Decimal
from src.components.threadpool_manager import global_threadpool


class AddRecordWindow(QtWidgets.QWidget):
    def __init__(self, func, func_2):
        super().__init__()

        self.close_add_record_window = func
        self.update_total_amount_on_dashboard_after_add_record = func_2

        self.setup_window()
        self.setup_container()
        self.setup_form_widgets()

    def setup_window(self):
        self.setFixedSize(QtCore.QSize(710, 410))
        self.setWindowIcon(QtGui.QIcon(":/assets/icons/unitrack_icon"))
        self.setStyleSheet(
            """
        background-color: #DBDBDB;
        font-weight: bold;
        color: #3B3B3B;
        """
        )
        self.setWindowTitle("UniTrack")

    def setup_container(self):
        self.container_layout = QtWidgets.QVBoxLayout(self)
        self.container_layout.setContentsMargins(10, 0, 10, 10)
        self.container_layout.setSpacing(10)

    def setup_form_widgets(self):
        self.grid_widget = QtWidgets.QWidget()
        self.grid_widget.setContentsMargins(0, 10, 0, 0)

        self.grid_layout = QtWidgets.QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setVerticalSpacing(20)

        self.service_number_label = QtWidgets.QLabel("Service Number")
        self.grid_layout.addWidget(self.service_number_label, 0, 0)

        self.service_number_container_widget = QtWidgets.QWidget()
        self.service_number_container_layout = QtWidgets.QHBoxLayout(
            self.service_number_container_widget
        )

        self.service_number_textbox = QtWidgets.QLineEdit()
        self.service_number_textbox.setFixedSize(QtCore.QSize(161, 35))
        self.service_number_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )

        self.search_button = QtWidgets.QPushButton()
        self.search_button.setObjectName("SearchButton")
        self.search_button.setFixedSize(QtCore.QSize(29, 34))
        self.search_button.setStyleSheet(
            """
                QPushButton#SearchButton {
                    background-color: #8B4513;
                    color: white;
                    font-weight: bold;
                    border-radius: 5;   
                }
                
                QPushButton#SearchButton:hover {
                    background-color: #67330E;
                    color: white;
                }
                
                QPushButton#SearchButton:pressed {
                    background-color: #B85B19;
                }
            """
        )
        self.search_icon = QtGui.QIcon(":/assets/icons/search")
        self.search_button.setIcon(self.search_icon)
        self.search_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.search_button.clicked.connect(self.search_employee)

        self.service_number_container_layout.addWidget(self.service_number_textbox)
        self.service_number_container_layout.addWidget(self.search_button)

        self.grid_layout.addWidget(self.service_number_container_widget, 0, 1)

        self.category_label = QtWidgets.QLabel("Category")
        self.grid_layout.addWidget(self.category_label, 0, 2)
        self.category_dropdown = QtWidgets.QComboBox()
        self.category_dropdown = setup_combobox(self.category_dropdown, "category")

        # Setting initial category value
        index = self.category_dropdown.findText("")
        self.category_dropdown.setCurrentIndex(index)

        self.category_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.category_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.category_dropdown, 0, 3)

        self.name_label = QtWidgets.QLabel("Name")
        self.grid_layout.addWidget(self.name_label, 1, 0)
        self.name_textbox = QtWidgets.QLineEdit()
        self.name_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.name_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.name_textbox, 1, 1)

        self.uniform_price_label = QtWidgets.QLabel("Uniform Price")
        self.grid_layout.addWidget(self.uniform_price_label, 1, 2)
        self.uniform_price_textbox = QtWidgets.QLineEdit()
        self.uniform_price_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.uniform_price_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.uniform_price_textbox.textChanged.connect(
            self.calculate_outstanding_amount
        )
        self.grid_layout.addWidget(self.uniform_price_textbox, 1, 3)

        self.gender_label = QtWidgets.QLabel("Gender")
        self.grid_layout.addWidget(self.gender_label, 2, 0)
        self.gender_dropdown = QtWidgets.QComboBox()
        self.gender_dropdown = setup_combobox(self.gender_dropdown, "gender")

        # Setting initial gender value
        index = self.gender_dropdown.findText("")
        self.gender_dropdown.setCurrentIndex(index)

        self.gender_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.gender_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.gender_dropdown, 2, 1)

        self.amount_deducted_label = QtWidgets.QLabel("Amount Deducted")
        self.grid_layout.addWidget(self.amount_deducted_label, 2, 2)
        self.amount_deducted_textbox = QtWidgets.QLineEdit()
        self.amount_deducted_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.amount_deducted_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.amount_deducted_textbox.textChanged.connect(
            self.calculate_outstanding_amount
        )
        self.grid_layout.addWidget(self.amount_deducted_textbox, 2, 3)

        self.unit_label = QtWidgets.QLabel("Unit")
        self.grid_layout.addWidget(self.unit_label, 3, 0)
        self.unit_dropdown = QtWidgets.QComboBox()
        self.unit_dropdown = setup_combobox(self.unit_dropdown, "unit")

        # Setting initial unit value
        index = self.unit_dropdown.findText("")
        self.unit_dropdown.setCurrentIndex(index)

        self.unit_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.unit_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.unit_dropdown, 3, 1)

        self.outstanding_amount_label = QtWidgets.QLabel("Outstanding Amount")
        self.grid_layout.addWidget(self.outstanding_amount_label, 3, 2)
        self.outstanding_amount_textbox = QtWidgets.QLineEdit(readOnly=True)
        self.outstanding_amount_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.outstanding_amount_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.outstanding_amount_textbox, 3, 3)

        self.grade_label = QtWidgets.QLabel("Grade")
        self.grid_layout.addWidget(self.grade_label, 4, 0)
        self.grade_dropdown = QtWidgets.QComboBox()
        self.grade_dropdown = setup_combobox(self.grade_dropdown, "grade")

        # Setting initial grade value
        index = self.grade_dropdown.findText("")
        self.grade_dropdown.setCurrentIndex(index)

        self.grade_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.grade_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.grade_dropdown, 4, 1)

        self.deduction_status_label = QtWidgets.QLabel("Deduction Status")
        self.grid_layout.addWidget(self.deduction_status_label, 4, 2)
        self.deduction_status_dropdown = QtWidgets.QComboBox()
        self.deduction_status_dropdown = setup_combobox(
            self.deduction_status_dropdown, "deduction_status"
        )

        # Setting retrieved value
        index = self.deduction_status_dropdown.findText("")
        self.deduction_status_dropdown.setCurrentIndex(index)

        self.deduction_status_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.deduction_status_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.deduction_status_dropdown, 4, 3)

        self.rank_label = QtWidgets.QLabel("Rank")
        self.grid_layout.addWidget(self.rank_label, 5, 0)
        self.rank_dropdown = QtWidgets.QComboBox()
        self.rank_dropdown = setup_combobox(self.rank_dropdown, "rank")

        # Setting initial rank value
        index = self.rank_dropdown.findText("")
        self.rank_dropdown.setCurrentIndex(index)

        self.rank_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.rank_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.rank_dropdown, 5, 1)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setObjectName("SaveButton")
        self.save_button.setFixedSize(QtCore.QSize(140, 35))
        self.save_button.setStyleSheet(
            """
                QPushButton#SaveButton {
                    background-color: #8B4513;
                    color: white;
                    font-weight: bold;
                    border-radius: 5;   
                }
                
                QPushButton#SaveButton:hover {
                    background-color: #67330E;
                    color: white;
                }
                
                QPushButton#SaveButton:pressed {
                    background-color: #B85B19;
                    color: white;
                }
            """
        )
        self.save_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.save_button.clicked.connect(self.save_record)
        self.grid_layout.addWidget(
            self.save_button, 5, 2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setObjectName("CancelButton")
        self.cancel_button.setFixedSize(QtCore.QSize(140, 35))
        self.cancel_button.setStyleSheet(
            """
                QPushButton#CancelButton {
                    background-color: white;
                    color: #8B4513;
                    font-weight: bold;
                    border-radius: 5;
                    border: 2pt solid #8B4513;
                }
                
                QPushButton#CancelButton:hover {
                    color: #B85B19;
                }
                
                QPushButton#CancelButton:pressed {
                    color: #67330E;
                    background-color: white;
                }
                
            """
        )
        self.cancel_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.cancel_button.clicked.connect(self.close_window)
        self.grid_layout.addWidget(
            self.cancel_button, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.loading_info_area_widget = QtWidgets.QWidget()
        self.loading_info_area_widget.setContentsMargins(0, 0, 0, 0)
        self.loading_info_area_layout = QtWidgets.QHBoxLayout(
            self.loading_info_area_widget
        )
        self.loading_info_area_layout.setContentsMargins(0, 0, 0, 0)

        self.stack_widget = QtWidgets.QWidget()
        self.info_label_stack = QtWidgets.QStackedLayout(self.stack_widget)
        self.info_label_stack.setContentsMargins(0, 0, 0, 0)

        self.empty_widget = QtWidgets.QWidget()

        self.info_label = QtWidgets.QLabel()
        self.info_label.wordWrap()

        self.info_label_stack.addWidget(self.empty_widget)
        self.info_label_stack.addWidget(self.info_label)

        self.loading_info_area_layout.addWidget(
            self.stack_widget, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.loading_indicator_box = QtWidgets.QLabel()
        self.loading_indicator_box.setFixedSize(45, 45)
        self.loading_indicator = QtGui.QMovie(":/assets/icons/spinner-gif")
        self.loading_indicator.setScaledSize(self.loading_indicator_box.size())
        self.loading_indicator_box.setMovie(self.loading_indicator)
        self.loading_indicator_box.setVisible(False)
        self.loading_indicator.stop()
        self.loading_info_area_layout.addWidget(
            self.loading_indicator_box, alignment=QtCore.Qt.AlignmentFlag.AlignRight
        )

        self.container_layout.addWidget(self.grid_widget, stretch=2)
        self.container_layout.addWidget(
            self.loading_info_area_widget,
            stretch=1,
        )

    def display_employee_data(self, response):
        self.loading_indicator.stop()
        self.loading_indicator_box.setVisible(False)

        self.info_label_stack.setCurrentIndex(1)

        if "error" in response:
            error = response.get("error")
            self.info_label.setText(error)
            employee_data_info_error(self.info_label)

            self.total_amount_deducted = Decimal("0.00")

            self.name_textbox.setText("")
            self.name_textbox.setReadOnly(False)

            self.outstanding_amount_textbox.setText("")
            self.outstanding_amount_textbox.setReadOnly(False)

            self.uniform_price_textbox.setText("")
            self.uniform_price_textbox.setReadOnly(False)

            self.amount_deducted_textbox.setText("")
            self.amount_deducted_textbox.setReadOnly(False)

            index = self.unit_dropdown.findText("")
            self.unit_dropdown.setCurrentIndex(index)
            self.unit_dropdown.setEnabled(True)

            index = self.category_dropdown.findText("")
            self.category_dropdown.setCurrentIndex(index)
            self.category_dropdown.setEnabled(True)

            index = self.gender_dropdown.findText("")
            self.gender_dropdown.setCurrentIndex(index)
            self.gender_dropdown.setEnabled(True)

            index = self.rank_dropdown.findText("")
            self.rank_dropdown.setCurrentIndex(index)
            self.rank_dropdown.setEnabled(True)

            index = self.deduction_status_dropdown.findText("")
            self.deduction_status_dropdown.setCurrentIndex(index)
            self.deduction_status_dropdown.setEnabled(True)

            index = self.grade_dropdown.findText("")
            self.grade_dropdown.setCurrentIndex(index)
            self.grade_dropdown.setEnabled(True)

            return

        self.info_label.setText("Record exists")
        employee_data_info_success(self.info_label)

        employee = response.get("employee")
        occurrences = response.get("occurrences")
        self.total_amount_deducted = calculate_total_amount_deducted(occurrences)

        self.name_textbox.setText(employee.get("name"))
        self.name_textbox.setReadOnly(True)

        unit_index = self.unit_dropdown.findText(employee.get("unit_name"))
        self.unit_dropdown.setCurrentIndex(unit_index)
        self.unit_dropdown.setEnabled(False)

        rank_index = self.rank_dropdown.findText(employee.get("rank_name"))
        self.rank_dropdown.setCurrentIndex(rank_index)
        self.rank_dropdown.setEnabled(False)

        gender_index = self.gender_dropdown.findText(employee.get("gender_name"))
        self.gender_dropdown.setCurrentIndex(gender_index)
        self.gender_dropdown.setEnabled(False)

        grade_index = self.grade_dropdown.findText(employee.get("grade_name"))
        self.grade_dropdown.setCurrentIndex(grade_index)
        self.grade_dropdown.setEnabled(False)

        category_index = self.category_dropdown.findText(employee.get("category_name"))
        self.category_dropdown.setCurrentIndex(category_index)
        self.category_dropdown.setEnabled(False)

        uniform_price = occurrences[0].get("uniform_price")
        display_uniform_price = f"{uniform_price:,.2f}"
        self.uniform_price_textbox.setText(display_uniform_price)
        self.uniform_price_textbox.setReadOnly(True)

    def get_employee(self, service_number):
        with SessionLocal() as db:
            result = retrieve_employee_record(db, service_number)
            return result

    def search_employee(self):
        self.loading_indicator.start()
        self.loading_indicator_box.setVisible(True)

        service_number = self.service_number_textbox.text()

        self.worker = Worker(self.get_employee, service_number)
        self.worker.signals.result.connect(self.display_employee_data)
        global_threadpool.start(self.worker)

    def calculate_outstanding_amount(self):
        uniform_price = self.uniform_price_textbox.text().replace(",", "") or Decimal(
            "0.00"
        )
        uniform_price = two_dp_decimal(uniform_price)

        if uniform_price == Decimal("0.00"):
            return

        amount_deducted = self.amount_deducted_textbox.text().replace(
            ",", ""
        ) or Decimal("0.00")
        amount_deducted = two_dp_decimal(amount_deducted)

        try:
            difference = uniform_price - (amount_deducted + self.total_amount_deducted)
        except AttributeError:
            try:
                difference = uniform_price - amount_deducted
            except TypeError:
                self.info_label_stack.setCurrentIndex(1)
                self.info_label.setText(f"Invalid digits")
                employee_data_info_error(self.info_label)
                return

        except TypeError:
            self.info_label_stack.setCurrentIndex(1)
            self.info_label.setText(f"Invalid digits")
            employee_data_info_error(self.info_label)
            return

        difference = two_dp_decimal(difference)
        display_difference = f"{difference:,.2f}"
        self.outstanding_amount_textbox.setText(display_difference)

        # Setting the deduction status
        if uniform_price == difference:
            deduction_status_index = self.deduction_status_dropdown.findText(
                "No Deduction"
            )
            self.deduction_status_dropdown.setCurrentIndex(deduction_status_index)

        elif difference.is_zero() or difference.is_signed():
            deduction_status_index = self.deduction_status_dropdown.findText(
                "Full Deduction"
            )
            self.deduction_status_dropdown.setCurrentIndex(deduction_status_index)

        elif not difference.is_zero():
            deduction_status_index = self.deduction_status_dropdown.findText(
                "Partial Deduction"
            )
            self.deduction_status_dropdown.setCurrentIndex(deduction_status_index)

    def update_dashboard(self, total_amount_deducted):
        # Update the Total Amount Deducted of an employee record if found on the dashboard when it's record is modified
        service_number = self.service_number_textbox.text()

        with SessionLocal() as db:
            employee_data = retrieve_employee_record(db, service_number)

        self.update_total_amount_on_dashboard_after_add_record(
            service_number, total_amount_deducted, employee_data
        )

    def run_total_amount_deducted_update(self, service_number):
        with SessionLocal() as db:
            result = get_total_amount_deducted_by_service_number(db, service_number)
            return result

    def save_operation_result(self, response):
        self.loading_indicator.stop()
        self.loading_indicator_box.setVisible(False)

        # Little hack so the info label is shown
        self.info_label_stack.setCurrentIndex(0)
        self.info_label_stack.setCurrentIndex(1)

        if isinstance(response, dict):
            error = response.get("error")
            self.info_label.setText(str(error))
            employee_data_info_error(self.info_label)
            return

        self.info_label.setText("Record saved")
        employee_data_info_success(self.info_label)

        # Update Total Amount Deducted
        service_number = self.service_number_textbox.text()

        self.update_total_amount_worker = Worker(
            self.run_total_amount_deducted_update, service_number
        )
        self.update_total_amount_worker.signals.result.connect(self.update_dashboard)
        global_threadpool.start(self.update_total_amount_worker)

    def add_record(self, record):
        with SessionLocal() as db:
            result = add_record(db, record)
            return result

    def save_record(self):
        self.info_label.setVisible(False)
        self.loading_indicator.start()
        self.loading_indicator_box.setVisible(True)

        record = {}
        record["service_number"] = self.service_number_textbox.text()
        record["name"] = self.name_textbox.text()
        record["unit"] = self.unit_dropdown.currentText()
        record["grade"] = self.grade_dropdown.currentText()
        record["gender"] = self.gender_dropdown.currentText()
        record["rank"] = self.rank_dropdown.currentText()
        record["category"] = self.category_dropdown.currentText()
        record["uniform_price"] = self.uniform_price_textbox.text().replace(",", "")
        record["amount_deducted"] = self.amount_deducted_textbox.text().replace(",", "")
        record["outstanding_amount"] = self.outstanding_amount_textbox.text().replace(
            ",", ""
        )
        record["deduction_status"] = self.deduction_status_dropdown.currentText()

        self.save_worker = Worker(self.add_record, record)
        self.save_worker.signals.result.connect(self.save_operation_result)
        global_threadpool.start(self.save_worker)

    def close_window(self):
        self.close_add_record_window()

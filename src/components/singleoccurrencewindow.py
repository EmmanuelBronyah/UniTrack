from PySide6 import QtWidgets, QtCore, QtGui
import resources
from src.utils import (
    setup_combobox,
    employee_data_info_error,
    employee_data_info_success,
    get_total_amount_deducted,
    set_total_amount_deducted_on_employee,
)
from src.components.workerclass import Worker
from src.database.db import SessionLocal
from src.crud.crud_employee_record import save_record, delete_record
from src.components.threadpool_manager import global_threadpool
from src.components.deletedialog import DeleteDialog


class SingleOccurrenceWindow(QtWidgets.QWidget):
    def __init__(
        self,
        occurrence,
        employee,
        employee_row_number,
        occurrence_row_id,
        func,
        func_2,
        func_3,
    ):
        super().__init__()

        self.occurrence = occurrence
        self.employee = employee
        self.employee_row_number_on_dashboard = employee_row_number
        self.occurrence_row_id = occurrence_row_id
        self.update_occurrence_window = func
        self.update_occurrences_and_remove_occurrence = func_2
        self.update_total_amount_on_dashboard = func_3

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
        self.grid_layout.setVerticalSpacing(15)

        service_number = self.employee["service_number"]
        self.service_number_label = QtWidgets.QLabel("Service Number")
        self.grid_layout.addWidget(self.service_number_label, 0, 0)
        self.service_number_textbox = QtWidgets.QLineEdit(text=service_number)
        self.service_number_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.service_number_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.service_number_textbox, 0, 1)

        category = self.employee["category_name"]
        self.category_label = QtWidgets.QLabel("Category")
        self.grid_layout.addWidget(self.category_label, 0, 2)
        self.category_dropdown = QtWidgets.QComboBox()
        self.category_dropdown = setup_combobox(self.category_dropdown, "category")

        # Setting initial category value
        index = self.category_dropdown.findText(category)
        self.category_dropdown.setCurrentIndex(index)

        self.category_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.category_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.category_dropdown, 0, 3)

        name = self.employee["name"]
        self.name_label = QtWidgets.QLabel("Name")
        self.grid_layout.addWidget(self.name_label, 1, 0)
        self.name_textbox = QtWidgets.QLineEdit(text=name)
        self.name_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.name_textbox.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.grid_layout.addWidget(self.name_textbox, 1, 1)

        uniform_price = self.occurrence["uniform_price"]
        display_uniform_price = f"{uniform_price:,.2f}"
        self.uniform_price_label = QtWidgets.QLabel("Uniform Price")
        self.grid_layout.addWidget(self.uniform_price_label, 1, 2)
        self.uniform_price_textbox = QtWidgets.QLineEdit(text=display_uniform_price)
        self.uniform_price_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.uniform_price_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.uniform_price_textbox, 1, 3)

        gender = self.employee["gender_name"]
        self.gender_label = QtWidgets.QLabel("Gender")
        self.grid_layout.addWidget(self.gender_label, 2, 0)
        self.gender_dropdown = QtWidgets.QComboBox()
        self.gender_dropdown = setup_combobox(self.gender_dropdown, "gender")

        # Setting initial gender value
        index = self.gender_dropdown.findText(gender)
        self.gender_dropdown.setCurrentIndex(index)

        self.gender_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.gender_dropdown.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.grid_layout.addWidget(self.gender_dropdown, 2, 1)

        amount_deducted = self.occurrence["amount_deducted"]
        display_amount_deducted = f"{amount_deducted:,.2f}"
        self.amount_deducted_label = QtWidgets.QLabel("Amount Deducted")
        self.grid_layout.addWidget(self.amount_deducted_label, 2, 2)
        self.amount_deducted_textbox = QtWidgets.QLineEdit(text=display_amount_deducted)
        self.amount_deducted_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.amount_deducted_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.amount_deducted_textbox, 2, 3)

        unit = self.employee["unit_name"]
        self.unit_label = QtWidgets.QLabel("Unit")
        self.grid_layout.addWidget(self.unit_label, 3, 0)
        self.unit_dropdown = QtWidgets.QComboBox()
        self.unit_dropdown = setup_combobox(self.unit_dropdown, "unit")

        # Setting initial unit value
        index = self.unit_dropdown.findText(unit)
        self.unit_dropdown.setCurrentIndex(index)

        self.unit_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.unit_dropdown.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.grid_layout.addWidget(self.unit_dropdown, 3, 1)

        outstanding_amount = self.occurrence["outstanding_amount"]
        display_outstanding_amount = f"{outstanding_amount:,.2f}"
        self.outstanding_amount_label = QtWidgets.QLabel("Outstanding Amount")
        self.grid_layout.addWidget(self.outstanding_amount_label, 3, 2)
        self.outstanding_amount_textbox = QtWidgets.QLineEdit(
            readOnly=True, text=display_outstanding_amount
        )
        self.outstanding_amount_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.outstanding_amount_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.outstanding_amount_textbox, 3, 3)

        grade = self.employee["grade_name"]
        self.grade_label = QtWidgets.QLabel("Grade")
        self.grid_layout.addWidget(self.grade_label, 4, 0)
        self.grade_dropdown = QtWidgets.QComboBox()
        self.grade_dropdown = setup_combobox(self.grade_dropdown, "grade")

        # Setting initial grade value
        index = self.grade_dropdown.findText(grade)
        self.grade_dropdown.setCurrentIndex(index)

        self.grade_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.grade_dropdown.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.grid_layout.addWidget(self.grade_dropdown, 4, 1)

        deduction_status = self.occurrence["deduction_status_name"]
        self.deduction_status_label = QtWidgets.QLabel("Deduction Status")
        self.grid_layout.addWidget(self.deduction_status_label, 4, 2)
        self.deduction_status_dropdown = QtWidgets.QComboBox()
        self.deduction_status_dropdown = setup_combobox(
            self.deduction_status_dropdown, "deduction_status"
        )

        # Setting retrieved value
        index = self.deduction_status_dropdown.findText(deduction_status)
        self.deduction_status_dropdown.setCurrentIndex(index)

        self.deduction_status_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.deduction_status_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.deduction_status_dropdown, 4, 3)

        rank = self.employee["rank_name"]
        self.rank_label = QtWidgets.QLabel("Rank")
        self.grid_layout.addWidget(self.rank_label, 5, 0)
        self.rank_dropdown = QtWidgets.QComboBox()
        self.rank_dropdown = setup_combobox(self.rank_dropdown, "rank")

        # Setting initial rank value
        index = self.rank_dropdown.findText(rank)
        self.rank_dropdown.setCurrentIndex(index)

        self.rank_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.rank_dropdown.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.grid_layout.addWidget(self.rank_dropdown, 5, 1)

        updated_at = self.occurrence["updated_at"]
        self.updated_at_label = QtWidgets.QLabel("Updated At")
        self.grid_layout.addWidget(self.updated_at_label, 5, 2)
        self.updated_at_textbox = QtWidgets.QLineEdit(
            readOnly=True, text=str(updated_at)
        )
        self.updated_at_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.updated_at_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.updated_at_textbox, 5, 3)

        created_at = self.occurrence["created_at"]
        self.created_at_label = QtWidgets.QLabel("Created At")
        self.grid_layout.addWidget(self.created_at_label, 6, 0)
        self.created_at_textbox = QtWidgets.QLineEdit(
            readOnly=True, text=str(created_at)
        )
        self.created_at_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.created_at_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.created_at_textbox, 6, 1)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setFixedSize(QtCore.QSize(140, 35))
        self.save_button.setStyleSheet(
            """
                background-color: #8B4513;
                color: white;
                font-weight: bold;
                border-radius: 5;
            """
        )
        self.save_button.clicked.connect(self.save_updated_record)
        self.grid_layout.addWidget(
            self.save_button, 6, 2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.delete_button = QtWidgets.QPushButton("Delete")
        self.delete_button.setFixedSize(QtCore.QSize(140, 35))
        self.delete_button.setStyleSheet(
            """
                background-color: white;
                color: #8B4513;
                font-weight: bold;
                border-radius: 5;
            """
        )
        self.delete_button.clicked.connect(self.open_delete_dialog)
        self.grid_layout.addWidget(
            self.delete_button, 6, 3, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.loading_info_area_widget = QtWidgets.QWidget()
        self.loading_info_area_widget.setContentsMargins(0, 0, 0, 0)
        self.loading_info_area_layout = QtWidgets.QHBoxLayout(
            self.loading_info_area_widget
        )
        self.loading_info_area_layout.setContentsMargins(0, 0, 0, 0)

        self.info_label = QtWidgets.QLabel("This is information")
        self.info_label.wordWrap()
        self.info_label.setVisible(False)
        self.loading_info_area_layout.addWidget(
            self.info_label, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
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

    def handle_error(self): ...

    def display_updated_values(self, response):
        self.loading_indicator_box.setVisible(False)
        self.loading_indicator.stop()

        if "error" in response:
            error = response.get("error")
            self.info_label.setText(str(error))
            employee_data_info_error(self.info_label)
            self.info_label.setVisible(True)
            return

        self.info_label.setText("Record saved.")
        employee_data_info_success(self.info_label)
        self.info_label.setVisible(True)

        occurrences = response.get("occurrences")
        employee = response.get("employee")

        occurrence_to_display = occurrences[self.occurrence_row_id]

        self.service_number_textbox.setText(employee.get("service_number"))

        self.name_textbox.setText(employee.get("name"))

        unit_index = self.unit_dropdown.findText(employee.get("unit_name"))
        self.unit_dropdown.setCurrentIndex(unit_index)

        rank_index = self.rank_dropdown.findText(employee.get("rank_name"))
        self.rank_dropdown.setCurrentIndex(rank_index)

        gender_index = self.gender_dropdown.findText(employee.get("gender_name"))
        self.gender_dropdown.setCurrentIndex(gender_index)

        grade_index = self.grade_dropdown.findText(employee.get("grade_name"))
        self.grade_dropdown.setCurrentIndex(grade_index)

        category_index = self.category_dropdown.findText(employee.get("category_name"))
        self.category_dropdown.setCurrentIndex(category_index)

        uniform_price = occurrence_to_display.get("uniform_price")
        display_uniform_price = f"{uniform_price:,.2f}"
        self.uniform_price_textbox.setText(display_uniform_price)

        amount_deducted = occurrence_to_display.get("amount_deducted")
        display_amount_deducted = f"{amount_deducted:,.2f}"
        self.amount_deducted_textbox.setText(display_amount_deducted)

        outstanding_amount = occurrence_to_display.get("outstanding_amount")
        display_outstanding_amount = f"{outstanding_amount:,.2f}"
        self.outstanding_amount_textbox.setText(display_outstanding_amount)

        deduction_status_index = self.deduction_status_dropdown.findText(
            occurrence_to_display.get("deduction_status_name")
        )
        self.deduction_status_dropdown.setCurrentIndex(deduction_status_index)

        self.created_at_textbox.setText(str(occurrence_to_display.get("created_at")))

        self.updated_at_textbox.setText(str(occurrence_to_display.get("updated_at")))

        # Update the occurrences in the Occurrence window since one of the occurrences has been modified
        self.update_occurrence_window(response)

        # Update Total Amount Figure on the dashboard since one of the occurrences has been modified
        row_number = self.employee_row_number_on_dashboard
        total_amount_deducted = employee.get("total_amount_deducted")

        self.update_total_amount_on_dashboard(row_number, total_amount_deducted)

    def update_data(self, updated_employee_data):
        with SessionLocal() as db:
            result = save_record(db, updated_employee_data)
            return result

    def save_updated_record(self):
        self.loading_indicator.start()
        self.loading_indicator_box.setVisible(True)

        self.updated_employee_record = {
            "employee_id": self.employee.get("id"),
            "service_number": self.service_number_textbox.text(),
            "name": self.name_textbox.text(),
            "gender": self.gender_dropdown.currentText(),
            "unit": self.unit_dropdown.currentText(),
            "grade": self.grade_dropdown.currentText(),
            "category": self.category_dropdown.currentText(),
            "rank": self.rank_dropdown.currentText(),
            "occurrence_id": self.occurrence.get("id"),
            "uniform_price": self.uniform_price_textbox.text().replace(",", ""),
            "amount_deducted": self.amount_deducted_textbox.text().replace(",", ""),
            "deduction_status": self.deduction_status_dropdown.currentText(),
        }

        self.save_record_worker = Worker(
            self.update_data,
            self.updated_employee_record,
        )
        self.save_record_worker.signals.result.connect(self.display_updated_values)
        self.save_record_worker.signals.error.connect(self.handle_error)
        global_threadpool.start(self.save_record_worker)

    def change_total_amount_deducted_on_dashboard(self, total_amount_deducted):
        # Update Total Amount Figure on the dashboard since one of the occurrences has been deleted
        row_number = self.employee_row_number_on_dashboard
        self.update_total_amount_on_dashboard(row_number, total_amount_deducted)

    def start_total_amount_deducted_calculation(self, employee_id):
        with SessionLocal() as db:
            total_amount_deducted = get_total_amount_deducted(db, employee_id)
            result = set_total_amount_deducted_on_employee(
                db, employee_id, total_amount_deducted
            )

            if result:
                db.commit()

            return total_amount_deducted

    def initiate_occurrence_record_removal(self, response):
        if response == "DELETED LAST OCCURRENCE AND ASSOCIATED EMPLOYEE":
            self.update_occurrences_and_remove_occurrence(
                response,
                self.occurrence_row_id,
                self.employee.get("id"),
                True,
            )
            return
        else:
            self.update_occurrences_and_remove_occurrence(
                response,
                self.occurrence_row_id,
                self.employee.get("id"),
                False,
            )

        # Calculate Total Amount Deducted after occurrence deletion
        self.worker = Worker(
            self.start_total_amount_deducted_calculation, self.employee.get("id")
        )
        self.worker.signals.result.connect(
            self.change_total_amount_deducted_on_dashboard
        )
        global_threadpool.start(self.worker)

    def delete_occurrence(self):
        with SessionLocal() as db:
            result = delete_record(
                db, self.occurrence.get("id"), self.employee.get("id")
            )
            return result

    def open_delete_dialog(self):
        self.delete_dialog = DeleteDialog(
            self.start_deletion, self.exit_dialog, parent=self
        )
        self.delete_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.delete_dialog.show()

    def start_deletion(self):
        # Close the Delete Dialog before deletion starts
        self.exit_dialog()

        self.delete_record_worker = Worker(self.delete_occurrence)
        self.delete_record_worker.signals.result.connect(
            self.initiate_occurrence_record_removal
        )
        global_threadpool.start(self.delete_record_worker)

    def exit_dialog(self):
        self.delete_dialog.close()

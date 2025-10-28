from PySide6 import QtWidgets, QtCore, QtGui
from src.utils import (
    deduction_exceeded_warning,
    employee_data_info_error,
    employee_data_info_success,
)
from src.crud.crud_employee_record import save_record
from src.database.db import SessionLocal
from src.components.workerclass import Worker
from src.components.singleoccurrencewindow import SingleOccurrenceWindow
from src.components.finaloccurrencewindow import FinalOccurrenceWindow
from src.utils import calculate_total_amount_deducted, final_occurrence_deduction_status


class OccurrenceWindow(QtWidgets.QMainWindow):
    def __init__(self, employee_data, func):
        super().__init__()

        self.employee_data = employee_data
        self.update_employee_data_on_dashboard = func

        self.setup_window()
        self.setup_container()
        self.setup_header()
        self.setup_occurrence_table()
        self.setup_final_occurrence_title()
        self.setup_final_record_widget()
        self.display_occurrences()

    def setup_window(self):
        self.setFixedSize(QtCore.QSize(950, 410))
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
        self.container_widget = QtWidgets.QWidget()
        self.container_widget.setContentsMargins(10, 5, 10, 5)

        self.container_layout = QtWidgets.QVBoxLayout(self.container_widget)
        self.container_layout.setContentsMargins(10, 0, 10, 10)
        self.container_layout.setSpacing(10)

        self.setCentralWidget(self.container_widget)

    def setup_header(self):
        self.top_row_widget = QtWidgets.QWidget()
        self.top_row_widget.setContentsMargins(0, 0, 0, 0)

        self.top_row_layout = QtWidgets.QHBoxLayout(self.top_row_widget)
        self.top_row_layout.setContentsMargins(0, 0, 0, 0)

        self.occurrence_text = QtWidgets.QLabel(
            "Occurrence", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.occurrence_text.setFixedSize(QtCore.QSize(125, 40))
        self.occurrence_text.setStyleSheet(
            """
                background-color: #ADADAD;
                padding: 0 10 0 10;
                color: #3B3B3B; 
                font-weight: bold; 
                border-radius: 10;
            """
        )

        self.top_row_layout.addWidget(
            self.occurrence_text, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.container_layout.addWidget(self.top_row_widget, stretch=1)

    def setup_occurrence_table(self):
        self.table_widget = QtWidgets.QWidget()
        self.table_widget.setContentsMargins(0, 0, 0, 0)
        self.table_widget.setStyleSheet(
            """
                background-color: #ADADAD;
                color: #3B3B3B; 
                font-weight: bold;
                font-size: 11pt;
                border-radius: 5;
                gridline-color: #3B3B3B;
            """
        )

        self.table_layout = QtWidgets.QVBoxLayout(self.table_widget)
        self.table_widget.setContentsMargins(0, 0, 0, 0)

        self.occurrence_table = QtWidgets.QTableWidget()
        self.occurrence_table.setContentsMargins(0, 0, 0, 0)
        self.occurrence_table.setColumnCount(6)
        self.occurrence_table.setHorizontalHeaderLabels(
            [
                "Service Number",
                "Name",
                "Category",
                "Uniform Price",
                "Amount Deducted",
                "Deduction Status",
            ]
        )
        self.occurrence_table.cellClicked.connect(self.open_single_occurrence_window)

        header = self.occurrence_table.horizontalHeader()

        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.occurrence_table.setAlternatingRowColors(True)
        self.occurrence_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.occurrence_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        self.table_layout.addWidget(self.occurrence_table)

        self.container_layout.addWidget(self.table_widget, stretch=4)

    def setup_final_occurrence_title(self):
        self.top_row_widget = QtWidgets.QWidget()
        self.top_row_widget.setContentsMargins(0, 0, 0, 0)

        self.top_row_layout = QtWidgets.QHBoxLayout(self.top_row_widget)
        self.top_row_layout.setContentsMargins(0, 0, 0, 0)

        self.occurrence_text = QtWidgets.QLabel(
            "Final Occurrence", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.occurrence_text.setFixedSize(QtCore.QSize(150, 40))
        self.occurrence_text.setStyleSheet(
            """
                background-color: #ADADAD;
                padding: 0 10 0 10;
                color: #3B3B3B; 
                font-weight: bold; 
                border-radius: 10;
            """
        )

        self.top_row_layout.addWidget(
            self.occurrence_text, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.container_layout.addWidget(self.top_row_widget, stretch=1)

    def setup_final_record_widget(self):
        self.final_record_widget = QtWidgets.QWidget()
        self.final_record_layout = QtWidgets.QVBoxLayout(self.final_record_widget)
        self.final_record_layout.setContentsMargins(0, 0, 0, 0)

        self.form_widget = QtWidgets.QWidget()
        self.form_widget.setContentsMargins(0, 0, 0, 0)
        self.form_layout = QtWidgets.QGridLayout(self.form_widget)
        self.form_layout.setContentsMargins(0, 0, 0, 0)

        self.service_number = self.employee_data["employee"]["service_number"]
        self.service_number_widget = QtWidgets.QWidget()
        self.service_number_layout = QtWidgets.QHBoxLayout(self.service_number_widget)
        self.service_number_label = QtWidgets.QLabel("Service Number:")
        self.service_number_input = QtWidgets.QLineEdit(
            readOnly=True, text=self.service_number
        )
        self.service_number_input.setFixedHeight(35)
        self.service_number_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.service_number_layout.addWidget(self.service_number_label)
        self.service_number_layout.addWidget(self.service_number_input)
        self.form_layout.addWidget(self.service_number_widget, 0, 0)

        self.name = self.employee_data["employee"]["name"]
        self.name_widget = QtWidgets.QWidget()
        self.name_layout = QtWidgets.QHBoxLayout(self.name_widget)
        self.name_label = QtWidgets.QLabel("Name:")
        self.name_input = QtWidgets.QLineEdit(readOnly=True, text=self.name)
        self.name_input.setFixedHeight(35)
        self.name_input.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_input)
        self.form_layout.addWidget(self.name_widget, 0, 1)

        self.category = self.employee_data["employee"]["category_name"]
        self.category_widget = QtWidgets.QWidget()
        self.category_layout = QtWidgets.QHBoxLayout(self.category_widget)
        self.category_label = QtWidgets.QLabel("Category:")
        self.category_input = QtWidgets.QLineEdit(readOnly=True, text=self.category)
        self.category_input.setFixedHeight(35)
        self.category_input.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.category_layout.addWidget(self.category_label)
        self.category_layout.addWidget(self.category_input)
        self.form_layout.addWidget(self.category_widget, 0, 2)

        self.uniform_price = self.employee_data["occurrences"][0]["uniform_price"]
        self.uniform_price_widget = QtWidgets.QWidget()
        self.uniform_price_layout = QtWidgets.QHBoxLayout(self.uniform_price_widget)
        self.uniform_price_label = QtWidgets.QLabel("Uniform Price:")
        self.uniform_price_input = QtWidgets.QLineEdit(
            readOnly=True, text=str(self.uniform_price)
        )
        self.uniform_price_input.setFixedHeight(35)
        self.uniform_price_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.uniform_price_layout.addWidget(self.uniform_price_label)
        self.uniform_price_layout.addWidget(self.uniform_price_input)
        self.form_layout.addWidget(self.uniform_price_widget, 1, 0)

        self.amount_deducted = calculate_total_amount_deducted(
            self.employee_data["occurrences"]
        )
        self.amount_deducted_widget = QtWidgets.QWidget()
        self.amount_deducted_layout = QtWidgets.QHBoxLayout(self.amount_deducted_widget)
        self.amount_deducted_label = QtWidgets.QLabel("Amount Deducted:")
        self.amount_deducted_input = QtWidgets.QLineEdit(
            readOnly=True, text=str(self.amount_deducted)
        )
        self.amount_deducted_input.setFixedHeight(35)
        self.amount_deducted_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.amount_deducted_layout.addWidget(self.amount_deducted_label)
        self.amount_deducted_layout.addWidget(self.amount_deducted_input)
        self.form_layout.addWidget(self.amount_deducted_widget, 1, 1)

        self.deduction_status = final_occurrence_deduction_status(
            self.uniform_price, self.amount_deducted
        )
        self.deduction_status_widget = QtWidgets.QWidget()
        self.deduction_status_layout = QtWidgets.QHBoxLayout(
            self.deduction_status_widget
        )
        self.deduction_status_label = QtWidgets.QLabel("Deduction Status:")
        self.deduction_status_input = QtWidgets.QLineEdit(
            readOnly=True, text=self.deduction_status[0]
        )
        self.deduction_status_input.setFixedHeight(35)
        self.deduction_status_input.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.deduction_status_layout.addWidget(self.deduction_status_label)
        self.deduction_status_layout.addWidget(self.deduction_status_input)
        self.form_layout.addWidget(self.deduction_status_widget, 1, 2)

        self.view_button = QtWidgets.QPushButton("View")
        self.view_button.setFixedHeight(25)
        self.view_button.setFixedWidth(45)
        self.view_button.setStyleSheet(
            """
                background-color: #8B4513;
                color: white;
                font-weight: bold;
                border-radius: 5;
                font-size: 8.5pt;
            """
        )
        self.view_button.clicked.connect(
            lambda: self.open_final_occurrence_window(self.employee_data)
        )
        self.form_layout.addWidget(
            self.view_button, 1, 3, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.final_record_layout.addWidget(self.form_widget)

        self.container_layout.addWidget(self.final_record_widget, stretch=1)

    def display_occurrences(self):
        number_of_occurrences = len(self.employee_data["occurrences"])
        number_of_columns = 6
        employee_data_keys = [
            "service_number",
            "name",
            "category_name",
            "uniform_price",
            "amount_deducted",
            "deduction_status",
        ]

        self.occurrence_table.setRowCount(number_of_occurrences)

        for row in range(number_of_occurrences):

            for column in range(number_of_columns):
                if employee_data_keys[column] == "service_number":
                    cell_value = self.employee_data["employee"]["service_number"]

                elif employee_data_keys[column] == "name":
                    cell_value = self.employee_data["employee"]["name"]

                elif employee_data_keys[column] == "category_name":
                    cell_value = self.employee_data["employee"]["category_name"]

                elif employee_data_keys[column] == "uniform_price":
                    cell_value = self.employee_data["occurrences"][row]["uniform_price"]

                elif employee_data_keys[column] == "amount_deducted":
                    cell_value = self.employee_data["occurrences"][row][
                        "amount_deducted"
                    ]

                elif employee_data_keys[column] == "deduction_status":
                    cell_value = self.employee_data["occurrences"][row][
                        "deduction_status_name"
                    ]

                self.occurrence_table.setItem(
                    row,
                    column,
                    QtWidgets.QTableWidgetItem(str(cell_value)),
                )

    def open_single_occurrence_window(self, row, column):
        occurrence_clicked = self.employee_data["occurrences"][row]
        employee_clicked = self.employee_data["employee"]
        self.single_occurrence_window = SingleOccurrenceWindow(
            occurrence=occurrence_clicked,
            employee=employee_clicked,
            occurrence_row_id=row,
            func=self.display_updated_data,
        )
        self.single_occurrence_window.show()

    def open_final_occurrence_window(self, employee_data):
        final_employee_dict = {
            "service_number": employee_data["employee"]["service_number"],
            "name": employee_data["employee"]["name"],
            "gender": employee_data["employee"]["gender_name"],
            "unit": employee_data["employee"]["unit_name"],
            "grade": employee_data["employee"]["grade_name"],
            "rank": employee_data["employee"]["rank_name"],
            "category": employee_data["employee"]["category_name"],
        }

        # Re-calculate Total Amount Deducted that is to be displayed when final occurrence window is opened
        total_amount_deducted = calculate_total_amount_deducted(
            employee_data["occurrences"]
        )

        final_occurrence_dict = {
            "uniform_price": str(employee_data["occurrences"][0]["uniform_price"]),
            "amount_deducted": str(total_amount_deducted),
            "outstanding_amount": self.deduction_status[1],
            "deduction_status": self.deduction_status[0],
        }
        self.single_occurrence_window = FinalOccurrenceWindow(
            occurrence=final_occurrence_dict, employee=final_employee_dict
        )
        self.single_occurrence_window.show()

    def display_updated_data(self, updated_data):
        self.employee_data = updated_data
        number_of_occurrences = len(self.employee_data["occurrences"])
        number_of_columns = 6
        employee_data_keys = [
            "service_number",
            "name",
            "category_name",
            "uniform_price",
            "amount_deducted",
            "deduction_status",
        ]

        self.occurrence_table.setRowCount(number_of_occurrences)

        for row in range(number_of_occurrences):

            for column in range(number_of_columns):
                if employee_data_keys[column] == "service_number":
                    cell_value = self.employee_data["employee"]["service_number"]

                elif employee_data_keys[column] == "name":
                    cell_value = self.employee_data["employee"]["name"]

                elif employee_data_keys[column] == "category_name":
                    cell_value = self.employee_data["employee"]["category_name"]

                elif employee_data_keys[column] == "uniform_price":
                    cell_value = self.employee_data["occurrences"][row]["uniform_price"]

                elif employee_data_keys[column] == "amount_deducted":
                    cell_value = self.employee_data["occurrences"][row][
                        "amount_deducted"
                    ]

                elif employee_data_keys[column] == "deduction_status":
                    cell_value = self.employee_data["occurrences"][row][
                        "deduction_status_name"
                    ]

                self.occurrence_table.setItem(
                    row,
                    column,
                    QtWidgets.QTableWidgetItem(str(cell_value)),
                )

        # Update final occurrence input boxes on occurrence window
        self.service_number_input.setText(
            self.employee_data["employee"]["service_number"]
        )
        self.name_input.setText(self.employee_data["employee"]["name"])
        self.category_input.setText(self.employee_data["employee"]["category_name"])
        self.uniform_price_input.setText(
            str(self.employee_data["occurrences"][row]["uniform_price"])
        )

        # Calculate and set Total Amount Deducted from the updated employee and occurrence data
        self.total_amount_deducted = calculate_total_amount_deducted(
            self.employee_data["occurrences"]
        )
        self.amount_deducted_input.setText(str(self.total_amount_deducted))

        # Calculate and set Deduction Status from the updated employee and occurrence data
        self.final_uniform_price = self.employee_data["occurrences"][row][
            "uniform_price"
        ]
        self.deduction_status = final_occurrence_deduction_status(
            self.final_uniform_price, self.total_amount_deducted
        )
        self.deduction_status_input.setText(self.deduction_status[0])

        # Update employee data on the dashboard
        self.update_employee_data_on_dashboard(updated_data["employee"])

from PySide6 import QtWidgets, QtCore, QtGui
import resources
from src.components.customlabel import CustomLabel
from src.components.occurrencewindow import OccurrenceWindow
from src.crud.crud_employee_record import (
    save_from_file,
    retrieve_random_records,
    retrieve_employee_record,
)
from src.database.db import SessionLocal
import os
from src.utils import (
    employee_data_info_success,
    employee_data_info_error,
    employee_data_info_warning,
)
from src.components.workerclass import Worker


class DashboardScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_dashboard_screen()

    def setup_window(self):
        self.setFixedSize(QtCore.QSize(950, 550))

    def setup_container(self):
        self.container_layout = QtWidgets.QVBoxLayout(self)
        self.container_layout.setContentsMargins(10, 0, 10, 10)

    def setup_top_row(self):
        self.top_row_widget = QtWidgets.QWidget()
        self.top_row_widget.setContentsMargins(0, 0, 0, 0)

        self.top_row_layout = QtWidgets.QHBoxLayout(self.top_row_widget)
        self.top_row_layout.setContentsMargins(0, 0, 0, 0)

        self.dashboard_text = QtWidgets.QLabel(
            "Dashboard", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.dashboard_text.setFixedSize(QtCore.QSize(125, 40))
        self.dashboard_text.setStyleSheet(
            """
                background-color: #ADADAD;
                padding: 0 10 0 10;
                color: #3B3B3B; 
                font-weight: bold; 
                border-radius: 10;
            """
        )

        self.search_layout = QtWidgets.QHBoxLayout()
        self.search_layout.setSpacing(0)
        self.search_layout.setContentsMargins(0, 0, 0, 0)

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setFixedWidth(455)
        self.search_bar.setStyleSheet(
            """
                background-color: #ADADAD; 
                padding: 8 0 8 10; 
                color: #3B3B3B; 
                font-weight: bold; 
                border-radius: 5;
            """
        )
        self.search_bar_button = QtWidgets.QPushButton()
        self.search_bar_button.setFixedSize(QtCore.QSize(50, 40))
        self.search_bar_button.setStyleSheet("background-color: #8B4513;")
        self.search_icon = QtGui.QIcon(":/assets/icons/search")
        self.search_bar_button.setIcon(self.search_icon)

        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_bar_button)

        self.profile_container = CustomLabel()
        self.profile_container.setStyleSheet("margin-right: 10;")
        self.profile_icon = QtGui.QPixmap(":/assets/icons/account")
        self.profile_container.setPixmap(self.profile_icon)

        self.top_row_layout.addWidget(self.dashboard_text)
        self.top_row_layout.addSpacing(120)
        self.top_row_layout.addLayout(self.search_layout)
        self.top_row_layout.addStretch()
        self.top_row_layout.addWidget(self.profile_container)

        self.container_layout.addWidget(self.top_row_widget, stretch=1)

    def setup_buttons_row(self):
        self.buttons_row_widget = QtWidgets.QWidget()
        self.buttons_row_widget.setContentsMargins(0, 0, 0, 0)

        self.buttons_row_layout = QtWidgets.QHBoxLayout(self.buttons_row_widget)
        self.buttons_row_layout.setContentsMargins(70, 0, 0, 0)
        self.buttons_row_layout.setSpacing(100)

        self.add_record_button = QtWidgets.QPushButton("Add record")
        self.add_record_button.setFixedHeight(40)
        self.add_record_button.setFixedWidth(120)
        self.add_record_button.setStyleSheet(
            """
                background-color: #8B4513;
                color: white;
                font-weight: bold;
                border-radius: 5;
            """
        )

        self.import_export_button_layout = QtWidgets.QHBoxLayout()
        self.import_export_button_layout.setSpacing(20)
        self.import_export_button_layout.setContentsMargins(0, 0, 0, 0)

        self.import_data_button = QtWidgets.QPushButton("Import data")
        self.import_data_button.setFixedHeight(40)
        self.import_data_button.setFixedWidth(120)
        self.import_data_button.setStyleSheet(
            """
                background-color: white;
                color: #8B4513;
                font-weight: bold;
                border-radius: 5;
                border: 2pt solid #8B4513;
            """
        )
        self.import_data_button.clicked.connect(self.import_data)

        self.export_button = QtWidgets.QPushButton("Export data")
        self.export_button.setFixedHeight(40)
        self.export_button.setFixedWidth(120)
        self.export_button.setStyleSheet(
            """
                background-color: #8B4513;
                color: white;
                font-weight: bold;
                border-radius: 5;
            """
        )

        self.import_export_button_layout.addWidget(self.import_data_button)
        self.import_export_button_layout.addWidget(self.export_button)

        self.buttons_row_layout.addWidget(self.add_record_button)
        self.buttons_row_layout.addLayout(self.import_export_button_layout)

        self.container_layout.addWidget(self.buttons_row_widget, stretch=1)

    def employee_records_table(self):
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

        self.employee_table = QtWidgets.QTableWidget()
        self.employee_table.setContentsMargins(0, 0, 0, 0)
        self.employee_table.setColumnCount(5)
        self.employee_table.setHorizontalHeaderLabels(
            [
                "Service Number",
                "Name",
                "Unit",
                "Grade",
                "Amount Deducted",
            ]
        )
        self.employee_table.cellClicked.connect(self.get_service_number_from_cell)

        header = self.employee_table.horizontalHeader()

        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.employee_table.setAlternatingRowColors(True)
        self.employee_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.employee_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.table_layout.addWidget(self.employee_table)

        self.container_layout.addWidget(self.table_widget, stretch=7)

    def footer_area(self):
        self.footer_widget = QtWidgets.QWidget()
        self.footer_widget.setContentsMargins(0, 0, 0, 0)

        self.footer_layout = QtWidgets.QHBoxLayout(self.footer_widget)
        self.footer_layout.setContentsMargins(0, 0, 0, 0)

        self.employee_data_info = QtWidgets.QLabel()
        self.employee_data_info.setWordWrap(True)
        self.employee_data_info.setVisible(False)
        self.employee_data_info.setStyleSheet(
            """
            background-color: #DBDBDB;
            color: white;
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
            self.employee_data_info,
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

    def load_employee_records_table_on_startup(self):
        self.loading_indicator.start()
        self.loading_indicator_box.setVisible(True)

        self.load_records_on_startup_worker = Worker(
            self.retrieve_records_from_database
        )
        self.threadpool = QtCore.QThreadPool()
        self.load_records_on_startup_worker.signals.result.connect(self.display_records)
        self.load_records_on_startup_worker.signals.error.connect(self.handle_error)
        self.threadpool.start(self.load_records_on_startup_worker)

    def show_employee_record_window(self, response):
        self.loading_indicator.stop()
        self.loading_indicator_box.setVisible(False)

        if "error" in response:
            error = response.get("error", None)
            self.employee_data_info.setText(f"{error}")
            employee_data_info_error(self.employee_data_info)
        else:
            self.employee_data_info.setText(f"Retrieved 1 employee record.")
            employee_data_info_success(self.employee_data_info)

            # show occurrence window
            self.occurrence_window = OccurrenceWindow(
                employee_data=response, func=self.display_modified_employee_data
            )
            self.occurrence_window.show()

    def get_employee_data(self, service_number):
        with SessionLocal() as db:
            result = retrieve_employee_record(db, service_number)
            return result

    def get_service_number_from_cell(self, row, column):
        self.loading_indicator.start()
        self.loading_indicator_box.setVisible(True)

        service_number_column = 0
        self.row_number_of_employee_clicked = row

        service_number = self.employee_table.item(
            self.row_number_of_employee_clicked, service_number_column
        ).text()

        get_employee_data_worker = Worker(self.get_employee_data, service_number)

        self.get_employee_data_threadpool = QtCore.QThreadPool()
        get_employee_data_worker.signals.result.connect(
            self.show_employee_record_window
        )
        get_employee_data_worker.signals.error.connect(self.handle_error)

        self.get_employee_data_threadpool.start(get_employee_data_worker)

    def display_records(self, records):
        self.loading_indicator.stop()
        self.loading_indicator_box.setVisible(False)

        if records is None:
            return

        number_of_rows = len(records)
        number_of_columns = 5
        self.employee_table.setRowCount(number_of_rows)

        for row in range(number_of_rows):

            for column in range(number_of_columns):
                headers = [
                    "service_number",
                    "name",
                    "unit",
                    "grade",
                    "total_amount_deducted",
                ]
                if headers[column] == "grade":
                    cell_value = records[row].grade_name
                elif headers[column] == "unit":
                    cell_value = records[row].unit_name
                else:
                    cell_value = records[row].__dict__.get(headers[column])

                self.employee_table.setItem(
                    row,
                    column,
                    QtWidgets.QTableWidgetItem(str(cell_value)),
                )

        self.employee_data_info.setVisible(True)
        self.employee_data_info.setText(f"Retrieved {number_of_rows} employee records.")
        employee_data_info_success(self.employee_data_info)

    def retrieve_records_from_database(self):
        with SessionLocal() as db:
            response = retrieve_random_records(db)
            return response

    def handle_records(self, response):
        self.loading_indicator.stop()
        self.loading_indicator_box.setVisible(False)

        error = response.get("error", None)
        records_saved = response.get("records saved", None)

        if error:
            self.employee_data_info.setText(f"{error}")
            employee_data_info_error(self.employee_data_info)
            self.employee_data_info.setVisible(True)
        else:
            self.employee_data_info.setText(
                f"Processed {records_saved if records_saved else '0'} records"
            )
            employee_data_info_success(self.employee_data_info)

        # Commence records retrieval from db
        self.loading_indicator.start()
        self.loading_indicator_box.setVisible(True)

        self.retrieve_records_worker = Worker(self.retrieve_records_from_database)

        self.retrieve_records_threadpool = QtCore.QThreadPool()
        self.retrieve_records_worker.signals.result.connect(self.display_records)
        self.retrieve_records_worker.signals.error.connect(self.handle_error)
        self.retrieve_records_threadpool.start(self.retrieve_records_worker)

    def handle_error(self, error_tuple):
        exception_type, value, traceback_str = error_tuple

        # exception_message = str(value.orig)
        # service_number = value.params[0]

        # error_message = integrity_error_message(exception_message, service_number)
        error_message = str(value)

        self.loading_indicator.stop()
        self.loading_indicator_box.setVisible(False)

        self.employee_data_info.setText(error_message)
        self.employee_data_info.setStyleSheet(
            """
            background-color: #dc3545;
            color: white;
            font-weight: bold; 
            border-radius: 5; 
            padding: 3;
            """
        )
        self.employee_data_info.setVisible(True)

    def import_data(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Records Excel File",
            desktop_path,
            "Excel Files (*.xlsx *.xls)",
        )
        if not file_path:
            self.employee_data_info.setText("No file selected")
            employee_data_info_error(self.employee_data_info)
            self.employee_data_info.setVisible(True)
            return

        self.loading_indicator.start()
        self.loading_indicator_box.setVisible(True)
        self.employee_data_info.setVisible(True)

        with SessionLocal() as db:
            save_from_file_worker = Worker(save_from_file, db, file_path)

            self.save_from_file_threadpool = QtCore.QThreadPool()
            save_from_file_worker.signals.result.connect(self.handle_records)
            save_from_file_worker.signals.error.connect(self.handle_error)

            self.save_from_file_threadpool.start(save_from_file_worker)

    def display_modified_employee_data(self, updated_data):
        number_of_columns = 5
        row = self.row_number_of_employee_clicked

        for column in range(number_of_columns):
            headers = [
                "service_number",
                "name",
                "unit",
                "grade",
                "total_amount_deducted",
            ]
            if headers[column] == "grade":
                cell_value = updated_data["grade_name"]
            elif headers[column] == "unit":
                cell_value = updated_data["unit_name"]
            else:
                cell_value = updated_data[headers[column]]

            self.employee_table.setItem(
                row,
                column,
                QtWidgets.QTableWidgetItem(str(cell_value)),
            )

    def setup_dashboard_screen(self):
        self.setup_container()
        self.setup_top_row()
        self.setup_buttons_row()
        self.employee_records_table()
        self.footer_area()
        self.load_employee_records_table_on_startup()

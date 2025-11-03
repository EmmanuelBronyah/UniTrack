from PySide6 import QtWidgets, QtCore, QtGui
import resources
from src.utils import (
    setup_combobox,
    employee_data_info_error,
    employee_data_info_success,
)
from src.components.workerclass import Worker
from src.database.db import SessionLocal
from src.crud.crud_employee_record import save_record, delete_record


class AddRecordWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

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

        self.service_number_label = QtWidgets.QLabel("Service Number")
        self.grid_layout.addWidget(self.service_number_label, 0, 0)
        self.service_number_textbox = QtWidgets.QLineEdit()
        self.service_number_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.service_number_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.service_number_textbox, 0, 1)

        self.category_label = QtWidgets.QLabel("Category")
        self.grid_layout.addWidget(self.category_label, 0, 2)
        self.category_dropdown = QtWidgets.QComboBox()
        self.category_dropdown = setup_combobox(self.category_dropdown, "category")

        # Setting initial category value
        index = self.category_dropdown.findText("")
        self.category_dropdown.setCurrentIndex(index)

        self.category_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.category_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.category_dropdown, 0, 3)

        self.name_label = QtWidgets.QLabel("Name")
        self.grid_layout.addWidget(self.name_label, 1, 0)
        self.name_textbox = QtWidgets.QLineEdit()
        self.name_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.name_textbox.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.grid_layout.addWidget(self.name_textbox, 1, 1)

        self.uniform_price_label = QtWidgets.QLabel("Uniform Price")
        self.grid_layout.addWidget(self.uniform_price_label, 1, 2)
        self.uniform_price_textbox = QtWidgets.QLineEdit()
        self.uniform_price_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.uniform_price_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
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
        self.gender_dropdown.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.grid_layout.addWidget(self.gender_dropdown, 2, 1)

        self.amount_deducted_label = QtWidgets.QLabel("Amount Deducted")
        self.grid_layout.addWidget(self.amount_deducted_label, 2, 2)
        self.amount_deducted_textbox = QtWidgets.QLineEdit()
        self.amount_deducted_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.amount_deducted_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
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
        self.unit_dropdown.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.grid_layout.addWidget(self.unit_dropdown, 3, 1)

        self.outstanding_amount_label = QtWidgets.QLabel("Outstanding Amount")
        self.grid_layout.addWidget(self.outstanding_amount_label, 3, 2)
        self.outstanding_amount_textbox = QtWidgets.QLineEdit(readOnly=True)
        self.outstanding_amount_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.outstanding_amount_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
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
        self.grade_dropdown.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
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
            "background-color: #ADADAD; color: #3B3B3B;"
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
        self.rank_dropdown.setStyleSheet("background-color: #ADADAD; color: #3B3B3B;")
        self.grid_layout.addWidget(self.rank_dropdown, 5, 1)

        self.updated_at_label = QtWidgets.QLabel("Updated At")
        self.grid_layout.addWidget(self.updated_at_label, 5, 2)
        self.updated_at_textbox = QtWidgets.QLineEdit(readOnly=True)
        self.updated_at_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.updated_at_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.updated_at_textbox, 5, 3)

        self.created_at_label = QtWidgets.QLabel("Created At")
        self.grid_layout.addWidget(self.created_at_label, 6, 0)
        self.created_at_textbox = QtWidgets.QLineEdit(readOnly=True)
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
        # self.save_button.clicked.connect(self.save_updated_record)
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
        # self.delete_button.clicked.connect(self.delete_record)
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

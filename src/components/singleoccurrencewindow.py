from PySide6 import QtWidgets, QtCore, QtGui
import resources
from src.utils import setup_combobox


class SingleOccurrenceWindow(QtWidgets.QWidget):
    def __init__(self, occurrence, employee):
        super().__init__()

        self.occurrence = occurrence
        self.employee = employee

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
        self.grid_widget.setContentsMargins(0, 0, 0, 0)

        self.grid_layout = QtWidgets.QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

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
        self.uniform_price_label = QtWidgets.QLabel("Uniform Price")
        self.grid_layout.addWidget(self.uniform_price_label, 1, 2)
        self.uniform_price_textbox = QtWidgets.QLineEdit(text=str(uniform_price))
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
        self.amount_deducted_label = QtWidgets.QLabel("Amount Deducted")
        self.grid_layout.addWidget(self.amount_deducted_label, 2, 2)
        self.amount_deducted_dropdown = QtWidgets.QLineEdit(text=str(amount_deducted))
        self.amount_deducted_dropdown.setFixedSize(QtCore.QSize(195, 35))
        self.amount_deducted_dropdown.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B;"
        )
        self.grid_layout.addWidget(self.amount_deducted_dropdown, 2, 3)

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
        self.outstanding_amount_label = QtWidgets.QLabel("Outstanding Amount")
        self.grid_layout.addWidget(self.outstanding_amount_label, 3, 2)
        self.outstanding_amount_textbox = QtWidgets.QLineEdit(
            text=str(outstanding_amount)
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
        self.grid_layout.addWidget(
            self.delete_button, 6, 3, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.container_layout.addWidget(self.grid_widget)

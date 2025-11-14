from PySide6 import QtWidgets, QtCore, QtGui
import resources
from decimal import Decimal


class FinalOccurrenceWindow(QtWidgets.QWidget):
    def __init__(self, occurrence, employee):
        super().__init__()

        self.occurrence = occurrence
        self.employee = employee

        self.setup_window()
        self.setup_container()
        self.setup_form_widgets()
        self.check_exceeded_deduction()

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
        self.service_number_textbox = QtWidgets.QLineEdit(
            readOnly=True, text=service_number
        )
        self.service_number_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.service_number_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.service_number_textbox, 0, 1)

        category = self.employee["category"]
        self.category_label = QtWidgets.QLabel("Category")
        self.grid_layout.addWidget(self.category_label, 0, 2)
        self.category_textbox = QtWidgets.QLineEdit(readOnly=True, text=category)
        self.category_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.category_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.category_textbox, 0, 3)

        name = self.employee["name"]
        self.name_label = QtWidgets.QLabel("Name")
        self.grid_layout.addWidget(self.name_label, 1, 0)
        self.name_textbox = QtWidgets.QLineEdit(readOnly=True, text=name)
        self.name_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.name_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.name_textbox, 1, 1)

        uniform_price = Decimal(self.occurrence["uniform_price"])
        display_uniform_price = f"{uniform_price:,.2f}"
        self.uniform_price_label = QtWidgets.QLabel("Uniform Price")
        self.grid_layout.addWidget(self.uniform_price_label, 1, 2)
        self.uniform_price_textbox = QtWidgets.QLineEdit(
            readOnly=True, text=display_uniform_price
        )
        self.uniform_price_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.uniform_price_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.uniform_price_textbox, 1, 3)

        gender = self.employee["gender"]
        self.gender_label = QtWidgets.QLabel("Gender")
        self.grid_layout.addWidget(self.gender_label, 2, 0)
        self.gender_textbox = QtWidgets.QLineEdit(readOnly=True, text=gender)
        self.gender_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.gender_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.gender_textbox, 2, 1)

        amount_deducted = Decimal(self.occurrence["amount_deducted"])
        display_amount_deducted = f"{amount_deducted:,.2f}"
        self.amount_deducted_label = QtWidgets.QLabel("Amount Deducted")
        self.grid_layout.addWidget(self.amount_deducted_label, 2, 2)
        self.amount_deducted_textbox = QtWidgets.QLineEdit(
            readOnly=True, text=display_amount_deducted
        )
        self.amount_deducted_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.amount_deducted_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.amount_deducted_textbox, 2, 3)

        unit = self.employee["unit"]
        self.unit_label = QtWidgets.QLabel("Unit")
        self.grid_layout.addWidget(self.unit_label, 3, 0)
        self.unit_textbox = QtWidgets.QLineEdit(readOnly=True, text=unit)
        self.unit_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.unit_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.unit_textbox, 3, 1)

        self.outstanding_amount = Decimal(self.occurrence["outstanding_amount"])
        display_outstanding_amount = f"{self.outstanding_amount:,.2f}"
        self.outstanding_amount_label = QtWidgets.QLabel("Outstanding Amount")
        self.grid_layout.addWidget(self.outstanding_amount_label, 3, 2)
        self.outstanding_amount_textbox = QtWidgets.QLineEdit(
            readOnly=True, text=display_outstanding_amount
        )
        self.outstanding_amount_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.outstanding_amount_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.outstanding_amount_textbox, 3, 3)

        grade = self.employee["grade"]
        self.grade_label = QtWidgets.QLabel("Grade")
        self.grid_layout.addWidget(self.grade_label, 4, 0)
        self.grade_textbox = QtWidgets.QLineEdit(readOnly=True, text=grade)
        self.grade_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.grade_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.grade_textbox, 4, 1)

        deduction_status = self.occurrence["deduction_status"]
        self.deduction_status_label = QtWidgets.QLabel("Deduction Status")
        self.grid_layout.addWidget(self.deduction_status_label, 4, 2)
        self.deduction_status_textbox = QtWidgets.QLineEdit(
            readOnly=True, text=deduction_status
        )
        self.deduction_status_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.deduction_status_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.deduction_status_textbox, 4, 3)

        rank = self.employee["rank"]
        self.rank_label = QtWidgets.QLabel("Rank")
        self.grid_layout.addWidget(self.rank_label, 5, 0)
        self.rank_textbox = QtWidgets.QLineEdit(readOnly=True, text=rank)
        self.rank_textbox.setFixedSize(QtCore.QSize(195, 35))
        self.rank_textbox.setStyleSheet(
            "background-color: #ADADAD; color: #3B3B3B; border-radius: 5; padding-left: 8px;"
        )
        self.grid_layout.addWidget(self.rank_textbox, 5, 1)

        self.exceeded_deduction_label = QtWidgets.QLabel("Exceeded Deduction")
        self.exceeded_deduction_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.exceeded_deduction_label.setStyleSheet(
            """
                background-color: #dc3545;
                padding: 0 10 0 10;
                color: #3B3B3B; 
                font-weight: bold; 
                border-radius: 10;
                color: white;
            """
        )
        self.exceeded_deduction_label.setVisible(False)
        self.grid_layout.addWidget(self.exceeded_deduction_label, 5, 3)

        self.container_layout.addWidget(self.grid_widget)

    def check_exceeded_deduction(self):
        if self.outstanding_amount.is_signed():
            self.exceeded_deduction_label.setVisible(True)
        else:
            self.exceeded_deduction_label.setVisible(False)

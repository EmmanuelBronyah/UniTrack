from PySide6 import QtCore, QtGui, QtWidgets


class DeleteDialog(QtWidgets.QDialog):

    def __init__(self, func, func_2, parent=None):
        super().__init__(parent)

        self.delete_record = func
        self.exit_dialog = func_2

        self.setup_window()
        self.setup_container()
        self.setup_widgets()

    def setup_window(self):
        self.setFixedSize(QtCore.QSize(400, 100))
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
        self.container_layout.setContentsMargins(0, 0, 0, 15)

    def setup_widgets(self):
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.delete_question = QtWidgets.QLabel(
            "Are you sure you want to delete this occurrence?"
        )
        self.main_layout.addWidget(
            self.delete_question, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)

        self.yes_button = QtWidgets.QPushButton("Yes")
        self.yes_button.setFixedSize(QtCore.QSize(140, 35))
        self.yes_button.clicked.connect(self.perform_deletion)
        self.yes_button.setStyleSheet(
            """
                background-color: #8B4513;
                color: white;
                font-weight: bold;
                border-radius: 5;
            """
        )

        self.buttons_layout.addWidget(self.yes_button)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setFixedSize(QtCore.QSize(140, 35))
        self.cancel_button.clicked.connect(self.close_dialog)
        self.cancel_button.setStyleSheet(
            """
                background-color: white;
                color: #8B4513;
                font-weight: bold;
                border-radius: 5;
            """
        )

        self.buttons_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(self.buttons_layout)

        self.container_layout.addWidget(self.main_widget)

    def perform_deletion(self):
        self.delete_record()

    def close_dialog(self):
        self.exit_dialog()

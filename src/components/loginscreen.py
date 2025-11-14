from PySide6 import QtWidgets, QtCore, QtGui
from src.crud.crud_user import login_user
from src.database.db import SessionLocal
import resources
from src.components.workerclass import Worker
from src.components.threadpool_manager import global_threadpool


class LoginScreen(QtWidgets.QWidget):
    login_success = QtCore.Signal(object)

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_login_screen()

    def setup_window(self):
        self.setFixedSize(QtCore.QSize(950, 550))

    def setup_container(self):
        self.container_layout = QtWidgets.QHBoxLayout(self)
        self.container_layout.setSpacing(250)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def setup_left_section(self):
        left_section_widget = QtWidgets.QWidget()
        left_section_widget.setContentsMargins(0, 0, 0, 0)

        left_section_layout = QtWidgets.QHBoxLayout(left_section_widget)
        left_section_layout.setSpacing(8)
        left_section_layout.setContentsMargins(70, 0, 0, 0)
        left_section_layout.setObjectName("leftSectionLayout")

        unitrack_label = QtWidgets.QLabel("UniTrack")
        unitrack_label.setObjectName("unitrackLabelLogin")

        icon_label = QtWidgets.QLabel()
        icon = QtGui.QPixmap(":/assets/icons/unitrack_icon")
        scaled_icon = icon.scaledToHeight(
            55, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        icon_label.setObjectName("iconLabel")
        icon_label.setPixmap(scaled_icon)

        left_section_layout.addWidget(unitrack_label)
        left_section_layout.addWidget(icon_label)

        self.container_layout.addWidget(
            left_section_widget, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

    def setup_right_section(self):
        right_section_widget = QtWidgets.QWidget()
        right_section_widget.setContentsMargins(0, 0, 0, 0)

        right_section_layout = QtWidgets.QVBoxLayout(right_section_widget)
        right_section_layout.setSpacing(60)
        right_section_layout.setContentsMargins(0, 0, 70, 0)

        # right top section(username and password text boxes)
        right_top_section_layout = QtWidgets.QVBoxLayout()
        right_top_section_layout.setSpacing(28)

        self.username_textbox = QtWidgets.QLineEdit()
        self.username_textbox.setObjectName("usernameTextbox")
        self.username_textbox.setFixedHeight(40)
        self.username_textbox.setFixedWidth(290)
        self.username_textbox.setPlaceholderText("Username")
        self.username_textbox.setStyleSheet("border-radius: 5; padding-left: 8px;")
        self.username_textbox.textEdited.connect(self.get_username)

        self.visible_icon = QtGui.QIcon(":/assets/icons/visible")
        self.hidden_icon = QtGui.QIcon(":/assets/icons/not_visible")

        self.password_textbox = QtWidgets.QLineEdit()
        self.password_textbox.setObjectName("passwordTextbox")
        self.password_textbox.setFixedHeight(40)
        self.password_textbox.setFixedWidth(290)
        self.password_textbox.setPlaceholderText("Password")
        self.password_textbox.setStyleSheet("border-radius: 5; padding-left: 8px;")
        self.password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_textbox.textEdited.connect(self.get_password)

        self.password_action = self.password_textbox.addAction(
            self.hidden_icon, QtWidgets.QLineEdit.TrailingPosition
        )
        self.password_action.triggered.connect(self.toggle_password_visibility)
        self.password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        right_top_section_layout.addWidget(self.username_textbox)
        right_top_section_layout.addWidget(self.password_textbox)

        right_section_layout.addLayout(right_top_section_layout)

        # right bottom section
        right_bottom_section_layout = QtWidgets.QVBoxLayout()
        right_bottom_section_layout.setSpacing(10)
        right_bottom_section_layout.setContentsMargins(0, 0, 32, 0)

        self.login_button = QtWidgets.QPushButton("LOGIN")
        self.login_button.setObjectName("loginButton")
        self.login_button.setFixedHeight(50)
        self.login_button.setFixedWidth(290)
        self.login_button.setStyleSheet("border-radius: 5;")
        self.login_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.perform_login)

        self.loader_info_widget = QtWidgets.QWidget()
        self.loader_info_widget.setContentsMargins(0, 0, 0, 0)

        self.loader_info_stack = QtWidgets.QStackedLayout(self.loader_info_widget)
        self.loader_info_stack.setContentsMargins(0, 0, 0, 0)

        self.spinner_box = QtWidgets.QLabel()
        self.spinner_box.setFixedSize(45, 45)
        self.movie = QtGui.QMovie(":/assets/icons/spinner-gif")
        self.movie.setScaledSize(self.spinner_box.size())
        self.spinner_box.setMovie(self.movie)

        self.empty_widget = QtWidgets.QWidget()

        self.info_box = QtWidgets.QLabel()

        self.loader_info_stack.addWidget(self.centered_widget(self.empty_widget))
        self.loader_info_stack.addWidget(self.centered_widget(self.spinner_box))
        self.loader_info_stack.addWidget(self.centered_widget(self.info_box))

        self.loader_info_stack.setCurrentIndex(0)

        right_bottom_section_layout.addWidget(self.login_button)
        right_bottom_section_layout.addWidget(
            self.loader_info_widget, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        right_section_layout.addLayout(right_bottom_section_layout)
        self.container_layout.addWidget(
            right_section_widget, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

    def setup_login_screen(self):
        self.setup_container()
        self.setup_left_section()
        self.setup_right_section()

    def centered_widget(self, widget):
        wrapper = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(45, 0, 0, 0)
        layout.addWidget(widget, alignment=QtCore.Qt.AlignCenter)
        return wrapper

    def toggle_password_visibility(self):
        if self.password_textbox.echoMode() == QtWidgets.QLineEdit.Password:
            self.password_textbox.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.password_action.setIcon(self.visible_icon)
        else:
            self.password_textbox.setEchoMode(QtWidgets.QLineEdit.Password)
            self.password_action.setIcon(self.hidden_icon)

    def get_username(self, text):
        self.username = text

    def get_password(self, text):
        self.password = text

    def handle_error(self, error_tuple):
        exctype, value, tb_str = error_tuple

        self.movie.stop()

        self.info_box.setText(str(value))
        self.info_box.setStyleSheet("color: #dc3545; font-weight: bold;")
        self.loader_info_stack.setCurrentIndex(2)

    def clear_text_boxes(self):
        self.username_textbox.clear()
        self.password_textbox.clear()
        delattr(self, "username")
        delattr(self, "password")
        self.loader_info_stack.setCurrentIndex(0)

    def handle_login(self, user):
        self.movie.stop()

        if user:
            self.info_box.setText("Login successful")
            self.info_box.setStyleSheet("color: #28a745; font-weight: bold;")
            self.loader_info_stack.setCurrentIndex(2)
            self.login_success.emit(user)

        else:
            self.info_box.setText("Invalid credentials")
            self.info_box.setStyleSheet("color: #dc3545; font-weight: bold;")
            self.loader_info_stack.setCurrentIndex(2)

    def perform_login(self):

        username = getattr(self, "username", "").strip()
        password = getattr(self, "password", "")

        if not username or not password:
            self.info_box.setText("Enter credentials")
            self.info_box.setStyleSheet("color: #dc3545; font-weight: bold;")
            self.loader_info_stack.setCurrentIndex(2)
            return

        self.movie.start()
        self.loader_info_stack.setCurrentIndex(1)

        with SessionLocal() as db:
            worker = Worker(login_user, db, username, password)
            worker.signals.result.connect(self.handle_login)
            worker.signals.error.connect(self.handle_error)
            global_threadpool.start(worker)

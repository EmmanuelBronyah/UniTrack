from PySide6 import QtWidgets, QtCore, QtGui
from src.crud.crud_user import login_user
from src.database.db import SessionLocal
from src import utils
import resources
from src.components.workerclass import Worker


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
        self.container_layout.setSpacing(170)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def setup_left_section(self):
        left_section_layout = QtWidgets.QHBoxLayout()
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

        self.container_layout.addLayout(left_section_layout)

    def setup_right_section(self):
        right_section_layout = QtWidgets.QVBoxLayout()
        right_section_layout.setSpacing(60)
        right_section_layout.setContentsMargins(0, 0, 70, 0)

        # right top section(username and password text boxes)
        right_top_section_layout = QtWidgets.QVBoxLayout()
        right_top_section_layout.setSpacing(28)

        username_textbox = QtWidgets.QLineEdit()
        username_textbox.setObjectName("usernameTextbox")
        username_textbox.setFixedHeight(40)
        username_textbox.setFixedWidth(290)
        username_textbox.setPlaceholderText("Username")
        username_textbox.textEdited.connect(self.get_username)

        # layout for password textbox and visibility icon button
        password_visibility_icon_box = QtWidgets.QHBoxLayout()
        password_visibility_icon_box.setSpacing(3)
        password_visibility_icon_box.setContentsMargins(0, 0, 0, 0)

        self.password_textbox = QtWidgets.QLineEdit()
        self.password_textbox.setObjectName("passwordTextbox")
        self.password_textbox.setFixedHeight(40)
        self.password_textbox.setFixedWidth(290)
        self.password_textbox.setPlaceholderText("Password")
        self.password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_textbox.textEdited.connect(self.get_password)

        self.visibility_button = QtWidgets.QToolButton()
        self.visibility_button.setObjectName("iconLabel")
        self.visibility_button.setFixedHeight(30)
        self.visibility_button.setFixedWidth(30)
        self.visibility_button.setCheckable(True)
        self.visibility_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        visibility_icon = QtGui.QIcon(":/assets/icons/visible")
        self.visibility_button.setIcon(visibility_icon)

        self.visibility_button.toggled.connect(self.toggle_password_visibility)

        password_visibility_icon_box.addWidget(self.password_textbox)
        password_visibility_icon_box.addWidget(self.visibility_button)

        right_top_section_layout.addWidget(username_textbox)
        right_top_section_layout.addLayout(password_visibility_icon_box)

        right_section_layout.addLayout(right_top_section_layout)

        # right bottom section
        right_bottom_section_layout = QtWidgets.QVBoxLayout()
        right_bottom_section_layout.setSpacing(10)
        right_bottom_section_layout.setContentsMargins(0, 0, 32, 0)

        self.login_button = QtWidgets.QPushButton("LOGIN")
        self.login_button.setObjectName("loginButton")
        self.login_button.setFixedHeight(50)
        self.login_button.setFixedWidth(290)
        self.login_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.perform_login)

        self.spinner_box = QtWidgets.QLabel()
        self.spinner_box.setFixedSize(45, 45)
        self.spinner_box.setVisible(False)

        self.movie = QtGui.QMovie(":/assets/icons/spinner-gif")
        self.movie.setScaledSize(self.spinner_box.size())
        self.spinner_box.setMovie(self.movie)

        self.info_box = QtWidgets.QLabel("Please enter username and password")
        self.info_box.setVisible(False)

        right_bottom_section_layout.addWidget(self.login_button)
        right_bottom_section_layout.addWidget(
            self.spinner_box, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        right_bottom_section_layout.addWidget(
            self.info_box, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        right_section_layout.addLayout(right_bottom_section_layout)
        self.container_layout.addLayout(right_section_layout)

    def setup_login_screen(self):
        self.setup_container()
        self.setup_left_section()
        self.setup_right_section()

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.visibility_button.setIcon(QtGui.QIcon(":/assets/icons/not_visible"))
        else:
            self.password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.visibility_button.setIcon(QtGui.QIcon(":/assets/icons/visible"))

    def get_username(self, text):
        self.username = text

    def get_password(self, text):
        self.password = text

    def handle_error(self, error_tuple):
        exctype, value, tb_str = error_tuple

        self.movie.stop()
        self.spinner_box.setVisible(False)

        self.info_box.setText(str(value))
        self.info_box.setStyleSheet("color: #dc3545; font-weight: bold;")
        self.info_box.setVisible(True)

    def handle_login(self, user):
        self.movie.stop()
        self.spinner_box.setVisible(False)

        if user:
            self.info_box.setText("Login was successful.")
            self.info_box.setStyleSheet("color: #28a745; font-weight: bold;")
            self.info_box.setVisible(True)
            self.login_success.emit(user)

        else:
            self.info_box.setText("Invalid username or password.")
            self.info_box.setStyleSheet("color: #dc3545; font-weight: bold;")
            self.info_box.setVisible(True)

    def perform_login(self):

        username = getattr(self, "username", "").strip()
        password = getattr(self, "password", "")

        if not username or not password:
            self.info_box.setText("Please enter username and password.")
            self.info_box.setStyleSheet("color: #dc3545; font-weight: bold;")
            self.info_box.setVisible(True)
            return

        self.movie.start()
        self.spinner_box.setVisible(True)
        self.info_box.setVisible(False)

        with SessionLocal() as db:
            worker = Worker(login_user, db, username, password)

            self.threadpool = QtCore.QThreadPool()
            worker.signals.result.connect(self.handle_login)
            worker.signals.error.connect(self.handle_error)

            self.threadpool.start(worker)

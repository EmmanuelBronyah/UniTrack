from PySide6 import QtWidgets, QtCore, QtGui
import utils


class LoginScreen(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_login_screen()

    def setup_window(self):
        self.setFixedSize(QtCore.QSize(950, 550))

    def setup_login_screen(self):
        container_layout = QtWidgets.QHBoxLayout(self)
        container_layout.setSpacing(170)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        left_section_layout = QtWidgets.QHBoxLayout()
        left_section_layout.setSpacing(8)
        left_section_layout.setContentsMargins(70, 0, 0, 0)
        left_section_layout.setObjectName("leftSectionLayout")

        unitrack_label = QtWidgets.QLabel("UniTrack")
        unitrack_label.setObjectName("unitrackLabelLogin")
        left_section_layout.addWidget(unitrack_label)

        icon_label = QtWidgets.QLabel()
        icon = QtGui.QPixmap("icons/icon.ico")
        scaled_icon = icon.scaledToHeight(
            55, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        icon_label.setObjectName("iconLabel")
        icon_label.setPixmap(scaled_icon)
        left_section_layout.addWidget(icon_label)

        container_layout.addLayout(left_section_layout)

        # right section
        right_section_layout = QtWidgets.QVBoxLayout()
        right_section_layout.setSpacing(60)
        right_section_layout.setContentsMargins(0, 0, 70, 0)

        # right tops section
        right_top_section_layout = QtWidgets.QVBoxLayout()
        right_top_section_layout.setSpacing(28)

        username_textbox = QtWidgets.QLineEdit()
        username_textbox.setObjectName("usernameTextbox")
        username_textbox.setFixedHeight(40)
        username_textbox.setFixedWidth(290)
        username_textbox.setPlaceholderText("Username")
        right_top_section_layout.addWidget(username_textbox)

        password_visibility_icon_box = QtWidgets.QHBoxLayout()
        password_visibility_icon_box.setSpacing(3)
        password_visibility_icon_box.setContentsMargins(0, 0, 0, 0)

        self.password_textbox = QtWidgets.QLineEdit()
        self.password_textbox.setObjectName("passwordTextbox")
        self.password_textbox.setFixedHeight(40)
        self.password_textbox.setFixedWidth(290)
        self.password_textbox.setPlaceholderText("Password")
        self.password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        password_visibility_icon_box.addWidget(self.password_textbox)

        self.visibility_button = QtWidgets.QToolButton()
        self.visibility_button.setFixedHeight(30)
        self.visibility_button.setFixedWidth(30)
        visibility_icon = QtGui.QIcon("icons/visible.svg")
        self.visibility_button.setIcon(visibility_icon)
        self.visibility_button.setObjectName("iconLabel")
        self.visibility_button.setCheckable(True)
        self.visibility_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.visibility_button.toggled.connect(self.toggle_password_visibility)
        password_visibility_icon_box.addWidget(self.visibility_button)

        right_top_section_layout.addLayout(password_visibility_icon_box)

        right_section_layout.addLayout(right_top_section_layout)

        # right bottom section
        right_bottom_section_layout = QtWidgets.QVBoxLayout()

        login_button = QtWidgets.QPushButton("LOGIN")
        login_button.setObjectName("loginButton")
        login_button.setFixedHeight(50)
        login_button.setFixedWidth(290)
        login_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        right_bottom_section_layout.addWidget(login_button)

        right_section_layout.addLayout(right_bottom_section_layout)

        container_layout.addLayout(right_section_layout)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.visibility_button.setIcon(QtGui.QIcon("icons/not_visible.svg"))
        else:
            self.password_textbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.visibility_button.setIcon(QtGui.QIcon("icons/visible.svg"))

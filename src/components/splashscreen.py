from PySide6 import QtWidgets, QtCore, QtGui
from src.crud.crud_user import create_user
from src.database.db import SessionLocal
from src.database.models import User
from src import utils
import resources


class SplashScreen(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.create_admin_user()
        self.setup_window()
        self.setup_logo_header()

    @staticmethod
    def create_admin_user():
        with SessionLocal() as db:
            users = db.query(User).all()
            if not users:
                admin_user = create_user(db, "010101", "Admin", "010101")
                return admin_user
            return

    def setup_window(self):
        self.setFixedSize(QtCore.QSize(950, 550))

    def setup_logo_header(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.unitrack_label = QtWidgets.QLabel("")
        self.unitrack_label.setObjectName("unitrackLabel")

        self.icon_label = QtWidgets.QLabel()
        icon = QtGui.QPixmap(":/assets/icons/unitrack_icon")
        scaled_icon = icon.scaledToHeight(
            75, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        self.icon_label.setObjectName("iconLabel")
        self.icon_label.setPixmap(scaled_icon)
        self.icon_label.setVisible(False)

        layout.addWidget(self.unitrack_label)
        layout.addWidget(self.icon_label)

        self.start_animation()

    def start_animation(self):
        full_text = "UniTrack"
        self.current_index = 0
        self.full_text = full_text

        self.typing_timer = QtCore.QTimer(self)
        self.typing_timer.timeout.connect(self.show_next_letter)
        self.typing_timer.start(160)

    def show_next_letter(self):
        if self.current_index < len(self.full_text):
            self.unitrack_label.setText(
                self.unitrack_label.text() + self.full_text[self.current_index]
            )
            self.current_index += 1
        else:
            self.typing_timer.stop()
            self.animate_icon()

    def animate_icon(self):
        self.icon_label.setVisible(True)
        self.icon_label.setGraphicsEffect(
            QtWidgets.QGraphicsOpacityEffect(self.icon_label)
        )
        self.icon_animation = QtCore.QPropertyAnimation(
            self.icon_label.graphicsEffect(), b"opacity"
        )
        self.icon_animation.setDuration(1000)
        self.icon_animation.setStartValue(0)
        self.icon_animation.setEndValue(1)
        self.icon_animation.start()

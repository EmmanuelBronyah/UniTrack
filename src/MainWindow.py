from PySide6 import QtWidgets, QtCore, QtGui
from src import utils
from src.components.splashscreen import SplashScreen
from src.components.loginscreen import LoginScreen
import resources


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        self.setWindowIcon(QtGui.QIcon(":/assets/icons/unitrack_icon"))
        self.setWindowTitle("UniTrack")
        self.setFixedSize(QtCore.QSize(950, 550))

    def setup_ui(self):
        self.stacked_widget = QtWidgets.QStackedWidget(self)

        self.splash_screen = SplashScreen()
        self.login_screen = LoginScreen()

        self.stacked_widget.addWidget(self.splash_screen)
        self.stacked_widget.addWidget(self.login_screen)

        self.stacked_widget.setCurrentIndex(0)

        self.setCentralWidget(self.stacked_widget)
        QtCore.QTimer.singleShot(
            3500,
            lambda: utils.show_screen(
                self.splash_screen,
                lambda: utils.fade_in_screen(self.stacked_widget, self.login_screen),
            ),
        )

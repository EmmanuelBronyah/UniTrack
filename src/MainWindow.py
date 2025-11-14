from PySide6 import QtWidgets, QtCore, QtGui
from src import utils
from src.components.splashscreen import SplashScreen
from src.components.loginscreen import LoginScreen
from src.components.dashboardscreen import DashboardScreen
import resources
from src.components.accountscreen import AccountScreen

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = "unitrack.unitrack.unitrack.version.1.0.0"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        self.login_screen.login_success.connect(self.show_dashboard)
        self.dashboard_screen.switch_to_account.connect(self.show_account_screen)
        self.account_screen.previous_screen.connect(self.switch_to_dashboard)
        self.account_screen.display_splashscreen.connect(self.switch_to_splashscreen)

    def setup_window(self):
        self.setWindowIcon(QtGui.QIcon(":/assets/icons/unitrack_icon"))
        self.setWindowTitle("UniTrack")
        self.setFixedSize(QtCore.QSize(950, 550))

    def setup_ui(self):
        self.stacked_widget = QtWidgets.QStackedWidget(self)

        self.splash_screen = SplashScreen()
        self.login_screen = LoginScreen()
        self.dashboard_screen = DashboardScreen()
        self.account_screen = AccountScreen()

        self.stacked_widget.addWidget(self.splash_screen)
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.dashboard_screen)
        self.stacked_widget.addWidget(self.account_screen)

        self.stacked_widget.setCurrentIndex(0)

        self.setCentralWidget(self.stacked_widget)
        QtCore.QTimer.singleShot(
            3500,
            lambda: utils.show_screen(
                self.splash_screen,
                lambda: utils.fade_in_screen(self.stacked_widget, self.login_screen),
            ),
        )

    def show_dashboard(self):
        QtCore.QTimer.singleShot(
            3500,
            lambda: utils.show_screen(
                self.login_screen,
                lambda: utils.fade_in_screen(
                    self.stacked_widget, self.dashboard_screen
                ),
            ),
        )

    def show_account_screen(self):
        self.stacked_widget.setCurrentIndex(3)

    def switch_to_dashboard(self):
        self.stacked_widget.setCurrentIndex(2)

    def switch_to_splashscreen(self):
        self.login_screen.clear_text_boxes()
        self.account_screen.get_username_from_db()

        QtCore.QTimer.singleShot(
            50,
            lambda: utils.show_screen(
                self.splash_screen,
                lambda: utils.fade_in_screen(self.stacked_widget, self.login_screen),
            ),
        )

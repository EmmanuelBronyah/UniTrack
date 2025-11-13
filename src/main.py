import sys
import os

# Ensure 'src' is discoverable before any imports
if getattr(sys, "frozen", False):
    # Running from PyInstaller exe
    base_path = sys._MEIPASS
else:
    # Running in dev
    base_path = os.path.abspath(os.path.dirname(__file__))

src_path = os.path.join(base_path, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)


from PySide6 import QtWidgets
from src.mainwindow import MainWindow
from src import utils


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Load styles
    utils.load_styles(app)

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()

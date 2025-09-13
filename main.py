import sys
from PySide6 import QtWidgets, QtGui
from MainWindow import MainWindow
import utils


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Load styles
    utils.load_styles(app)

    window = MainWindow()
    window.show()
    app.exec()


main()

from PySide6 import QtWidgets, QtGui, QtCore
import resources


def load_fonts():
    lato_font_path = ":/assets/fonts/lato"
    oswald_font_path_bold = ":/assets/fonts/oswald_bold"

    QtGui.QFontDatabase.addApplicationFont(lato_font_path)
    QtGui.QFontDatabase.addApplicationFont(oswald_font_path_bold)


def load_styles(app):

    load_fonts()
    app.setFont("Lato")

    file = QtCore.QFile(":/assets/styles/style")
    if file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
        stream = QtCore.QTextStream(file)
        app.setStyleSheet(stream.readAll())
        file.close()


_animations = []


def show_screen(screen, func):
    opacity_effect = QtWidgets.QGraphicsOpacityEffect(screen)
    screen.setGraphicsEffect(opacity_effect)
    fade_out = QtCore.QPropertyAnimation(opacity_effect, b"opacity")
    fade_out.setDuration(1000)
    fade_out.setStartValue(1)
    fade_out.setEndValue(0)
    fade_out.finished.connect(func)
    _animations.append(fade_out)
    fade_out.start()


def fade_in_screen(stacked_widget, login_screen):
    stacked_widget.setCurrentIndex(1)
    opacity_effect = QtWidgets.QGraphicsOpacityEffect(login_screen)
    login_screen.setGraphicsEffect(opacity_effect)
    fade_in = QtCore.QPropertyAnimation(opacity_effect, b"opacity")
    fade_in.setDuration(1000)
    fade_in.setStartValue(0)
    fade_in.setEndValue(1)
    _animations.append(fade_in)
    fade_in.start()

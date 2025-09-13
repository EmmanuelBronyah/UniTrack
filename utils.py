from PySide6 import QtWidgets, QtGui, QtCore


def load_fonts():
    lato_font_path = "fonts/Lato/Lato-Regular.ttf"
    oswald_font_path = "fonts/Oswald/Oswald-Bold.ttf"

    QtGui.QFontDatabase.addApplicationFont(lato_font_path)
    QtGui.QFontDatabase.addApplicationFont(oswald_font_path)


def load_styles(app):

    load_fonts()
    app.setFont("Lato")

    with open("styles/style.qss", "r") as f:
        app.setStyleSheet(f.read())


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

import os
import sys

from PyQt6 import QtWidgets, QtGui
from jukebox_client.views import MainView
from jukebox_client.config import CONFIG
from jukebox_client.controllers import MainController

ASSETS = os.path.join(os.getcwd(), "assets")
STYLESHEET = os.path.join(ASSETS, "styles", "stylesheet.qss")
FONTS = os.path.join(ASSETS, "fonts")


def load_fonts():
    for file in os.listdir(FONTS):
        font = os.path.join(FONTS, file)
        QtGui.QFontDatabase.addApplicationFont(font)


def main():
    app = QtWidgets.QApplication(sys.argv)

    load_fonts()

    with open(STYLESHEET) as f:
        style = f.read()

    for color_name, color in CONFIG.colors.dict().items():
        style = style.replace(f"%{color_name}%", color)

    app.setStyleSheet(style)

    main_view = MainView()
    ctrl = MainController(main_view)
    main_view.show()

    app.exec()


if __name__ == "__main__":
    main()

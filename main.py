import logging
import os
import sys

from PyQt6 import QtGui, QtWidgets

from jukebox_client.config import ASSETS, CONFIG
from jukebox_client.controllers import MainController
from jukebox_client.log import setup_basic_logger

STYLESHEET = os.path.join(ASSETS, "styles", "stylesheet.qss")
FONTS = os.path.join(ASSETS, "fonts")

log_file = os.path.join(
    os.getcwd(),
    CONFIG.general.log_directory,
    "disco_express_log.log",
)
os.makedirs(os.path.dirname(log_file), exist_ok=True)
setup_basic_logger(log_file)


def load_fonts():
    for file in os.listdir(FONTS):
        font = os.path.join(FONTS, file)
        QtGui.QFontDatabase.addApplicationFont(font)


def main():
    app = QtWidgets.QApplication(sys.argv)

    load_fonts()

    with open(STYLESHEET) as f:
        style = f.read()

    for color_name, color in CONFIG.style.colors.dict().items():
        style = style.replace(f"%{color_name}%", color)

    app.setStyleSheet(style)

    CONFIG.selected_language = CONFIG.languages[0]

    ctrl = MainController()
    ctrl.view.showFullScreen()
    try:
        app.exec()
    except BaseException:
        logging.exception("Base Exception ocurred")


if __name__ == "__main__":
    main()

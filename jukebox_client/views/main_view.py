import os

from PyQt6 import QtCore, QtGui, QtWidgets

from jukebox_client.config import CONFIG
from jukebox_client.views.widgets import (
    IconButton,
    TimeWidget,
    TitleLabel,
)

from .view import View


class MainView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainView")

        self._build_ui()
        self.background = QtGui.QPixmap(
            os.path.join(os.getcwd(), CONFIG.style.background_image),
        )
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

    def paintEvent(self, event: QtGui.QPaintEvent):  # noqa: N802, ARG002, inherited
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )
        self.setLayout(layout)

        header_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(header_layout)

        self.home_button = IconButton(
            CONFIG.icons.home_icon,
            CONFIG.style.colors.text_color,
            128,
        )
        header_layout.addWidget(self.home_button)

        self.time_widget = TimeWidget()
        header_layout.addWidget(self.time_widget)

        header_layout.addStretch()

        self.title = TitleLabel("Disco Express")
        header_layout.addWidget(self.title)

        header_layout.addStretch()

        self.date_widget = TimeWidget(time_format="%d.%m.%y")
        header_layout.addWidget(self.date_widget)

        self.stack = QtWidgets.QStackedWidget()
        layout.addWidget(self.stack)

    def add_page(self, page: View) -> int:
        self.stack.addWidget(page)
        return self.stack.count() - 1

    def closeEvent(self, event: QtGui.QCloseEvent):  # noqa: N802, inherited
        """Override the close event to prevent closing."""
        event.ignore()  # Ignore the close event

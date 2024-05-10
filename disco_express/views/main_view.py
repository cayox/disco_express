import os

from PyQt6 import QtCore, QtGui, QtWidgets

from disco_express.config import APP_CONFIG_ROOT, CONFIG
from disco_express.views.widgets import IconButton, TimeWidget, TitleLabel

from .view import View


class CentralWidget(QtWidgets.QWidget):
    """The central widget of the MainView, with a custom background.

    Configurable via the config.toml:
    - CONFIG.style.background_image
    - CONFIG.style.background_darkness_factor
    """
    def __init__(self):
        super().__init__()

        self.setObjectName("MainView")
        self.background = QtGui.QPixmap(
            os.path.join(APP_CONFIG_ROOT, CONFIG.style.background_image),
        )
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

    def paintEvent(self, event: QtGui.QPaintEvent):  # noqa: N802, ARG002, inherited
        """Draw the widget with the custom background."""
        painter = QtGui.QPainter(self)
        painter.setOpacity(1 - CONFIG.style.background_darkness_factor)
        painter.drawPixmap(self.rect(), self.background)


class MainView(QtWidgets.QMainWindow):
    """The main view holding all other views."""
    def __init__(self):
        super().__init__()
        self.setObjectName("MainView")

        self._build_ui()

    def _build_ui(self):
        self.widget = CentralWidget()
        self.setCentralWidget(self.widget)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )
        self.widget.setLayout(layout)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(32, 12, 32, 12)
        layout.addLayout(header_layout)

        self.home_button = IconButton(
            CONFIG.icons.home_icon,
            CONFIG.style.colors.accent1_glow,
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
        """Method to add a view to the application."""
        self.stack.addWidget(page)
        return self.stack.count() - 1

    def closeEvent(self, event: QtGui.QCloseEvent):  # noqa: N802, inherited
        """Override the close event to prevent closing."""
        event.ignore()  # Ignore the close event

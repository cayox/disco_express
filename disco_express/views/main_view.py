import logging
import os
import sys

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
        logging.info("Ignoring close event")
        event.ignore()  # Ignore the close event

    def keyPressEvent(self, event: QtGui.QKeyEvent):  # noqa: N802, inherited
        """Custom Key Event handler, to ignore common keyboard shortcuts to kill the app or get it out of focus."""
        # Define the secret shortcut Ctrl+Alt+Shift+Q
        if event.key() == QtCore.Qt.Key.Key_Q and event.modifiers() == (
            QtCore.Qt.KeyboardModifier.ControlModifier
            | QtCore.Qt.KeyboardModifier.AltModifier
            | QtCore.Qt.KeyboardModifier.ShiftModifier
        ):
            logging.info("Closing app through keyboard shortcut")
            sys.exit(0)

        # Block common system shortcuts on Raspbian OS
        if (
            event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier
            and event.key()
            in [
                QtCore.Qt.Key.Key_Tab,
                QtCore.Qt.Key.Key_W,
                QtCore.Qt.Key.Key_Q,
                QtCore.Qt.Key.Key_T,
                QtCore.Qt.Key.Key_L,
                QtCore.Qt.Key.Key_Escape,
            ]
            or event.modifiers()
            == (
                QtCore.Qt.KeyboardModifier.AltModifier
                | QtCore.Qt.KeyboardModifier.ControlModifier
            )
            and event.key() == QtCore.Qt.Key.Key_Delete
            or (
                event.modifiers() == QtCore.Qt.KeyboardModifier.AltModifier
                and event.key()
                in [
                    QtCore.Qt.Key.Key_Tab,
                    QtCore.Qt.Key.Key_F4,
                    QtCore.Qt.Key.Key_F2,
                    QtCore.Qt.Key.Key_Escape,
                    QtCore.Qt.Key.Key_F7,
                    QtCore.Qt.Key.Key_F10,
                ]
                or event.modifiers() == QtCore.Qt.KeyboardModifier.AltModifier
                and event.key() == QtCore.Qt.Key.Key_Print
            )
            or event.modifiers() == QtCore.Qt.KeyboardModifier.MetaModifier
            and event.key()
            in [
                QtCore.Qt.Key.Key_Space,
                QtCore.Qt.Key.Key_L,
                QtCore.Qt.Key.Key_D,
                QtCore.Qt.Key.Key_Tab,
                QtCore.Qt.Key.Key_Escape,
            ]
        ):
            event.ignore()
        else:
            super().keyPressEvent(event)

    def eventFilter(  # noqa: N802, inherited
        self,
        source: QtCore.QObject,
        event: QtCore.QEvent,
    ) -> bool:
        """Overwrite the event filter to add custom keypress handler."""
        if event.type() == QtCore.QEvent.Type.KeyPress:
            self.keyPressEvent(event)
            return True
        return super().eventFilter(source, event)
